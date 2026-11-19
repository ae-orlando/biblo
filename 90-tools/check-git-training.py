#!/usr/bin/env python3
"""Read selected evidence from an explicitly marked learner Git sandbox. No repair/write commands."""
import argparse
import json
import os
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('repository')
args=parser.parse_args()
repo=(ROOT/args.repository).resolve()
boundary=(ROOT/'03-exercises/git').resolve()
if not repo.is_relative_to(boundary) or not (repo/'.git').is_dir() or (repo/'.git').is_symlink():
    parser.error('choose an ordinary learner repository inside 03-exercises/git; no repository is initialized automatically')
marker=repo/'.vault-training'
if marker.is_symlink() or not marker.is_file() or marker.read_text().strip()!='git-practice':
    parser.error('expected the deliberate .vault-training marker from the lab')
env={key:value for key,value in os.environ.items() if not key.startswith('GIT')}
env.update(GIT_OPTIONAL_LOCKS='0',GIT_CONFIG_GLOBAL=os.devnull,GIT_CONFIG_SYSTEM=os.devnull,GIT_TERMINAL_PROMPT='0')


def git(*arguments,ok=True):
    result=subprocess.run(['git','--no-pager','-c','core.fsmonitor=false','-c',f'core.hooksPath={os.devnull}','-C',str(repo),*arguments],capture_output=True,text=True,env=env,timeout=10)
    if ok and result.returncode: raise SystemExit(result.stderr)
    return result


if Path(git('rev-parse','--show-toplevel').stdout.strip()).resolve()!=repo:
    raise SystemExit('Repository root does not match the selected sandbox')
policy=repo/'policy.txt'
parents=git('log','--format=%P').stdout.splitlines()
tracked=git('ls-files','-z').stdout.split('\0')
branches=set(git('branch','--format=%(refname:short)').stdout.splitlines())
checks={
    'main_checked_out':git('branch','--show-current').stdout.strip()=='main',
    'feature_branch_preserved':{'main','feature-limit'}<=branches,
    'merge_in_history':any(len(line.split())>=2 for line in parents),
    'final_policy':policy.is_file() and not policy.is_symlink() and policy.read_text()=='limit=35\n',
    'fake_env_not_tracked':'.env' not in tracked,
    'training_env_exists':(repo/'.env').is_file() and not (repo/'.env').is_symlink(),
    'fake_env_ignored':git('check-ignore','--quiet','--','.env',ok=False).returncode==0,
    'intended_worktree_clean':not git('status','--porcelain=v1').stdout,
}
print(json.dumps(checks,indent=2))
print('Read-only artifact checks only. Review the required diffs, graph, conflict and revert explanations separately.')
raise SystemExit(int(not all(checks.values())))
