CREATE FUNCTION transfer(source_id bigint, target_id bigint, amount bigint)
RETURNS void LANGUAGE plpgsql AS $$
DECLARE locked_count integer;
BEGIN
  IF amount IS NULL OR amount <= 0 OR source_id IS NULL OR target_id IS NULL OR source_id = target_id THEN
    RAISE EXCEPTION 'invalid transfer';
  END IF;
  -- Every caller locks the same pair in the same order.
  PERFORM id FROM accounts WHERE id IN (source_id,target_id) ORDER BY id FOR UPDATE;
  GET DIAGNOSTICS locked_count = ROW_COUNT;
  IF locked_count <> 2 THEN RAISE EXCEPTION 'account missing'; END IF;
  UPDATE accounts SET balance = balance - amount WHERE id = source_id AND balance >= amount;
  IF NOT FOUND THEN RAISE EXCEPTION 'insufficient funds'; END IF;
  UPDATE accounts SET balance = balance + amount WHERE id = target_id;
END;
$$;
