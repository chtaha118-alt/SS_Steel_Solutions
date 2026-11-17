-- Run once in Supabase > SQL Editor (lets a new customer create their own customer row)
create policy "customer self insert" on customers
  for insert to authenticated
  with check (user_id = auth.uid());
