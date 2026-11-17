-- SS STEEL SOLUTIONS: run this whole file once in Supabase > SQL Editor

create table if not exists profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  full_name text,
  phone text,
  role text not null default 'customer' check (role in ('admin','staff','customer'))
);

create table if not exists products (
  id bigint generated always as identity primary key,
  name text not null,
  category text not null check (category in ('plate','round_bar','rebar','square_bar','flat_bar','pipe','angle','beam')),
  size_label text,                       -- e.g. '12 mm', '48.3x3.2'
  grade text,
  price_per_kg numeric(10,2) not null default 0,
  stock_pieces int not null default 0,
  stock_kg numeric(12,3) not null default 0
);

create table if not exists inward_stock (
  id bigint generated always as identity primary key,
  product_id bigint references products(id),
  supplier text,
  heat_number text,
  pieces int not null,
  weight_kg numeric(12,3) not null,
  received_at timestamptz default now()
);

create table if not exists cutting_jobs (
  id bigint generated always as identity primary key,
  product_id bigint references products(id),
  input_pieces int not null,
  input_kg numeric(12,3) not null,
  output_kg numeric(12,3) not null,
  reusable_kg numeric(12,3) not null default 0,
  scrap_kg numeric(12,3) not null default 0,
  created_at timestamptz default now()
);

create table if not exists leftovers (
  id bigint generated always as identity primary key,
  product_id bigint references products(id),
  length_m numeric(10,3) not null,
  weight_kg numeric(12,3) not null,
  available boolean not null default true
);

create table if not exists scrap (
  id bigint generated always as identity primary key,
  cutting_job_id bigint references cutting_jobs(id),
  weight_kg numeric(12,3) not null,
  value numeric(12,2) not null default 0
);

create table if not exists customers (
  id bigint generated always as identity primary key,
  user_id uuid references auth.users(id),
  name text not null,
  phone text,
  address text
);

create table if not exists orders (
  id bigint generated always as identity primary key,
  customer_id bigint references customers(id),
  product_id bigint references products(id),
  quantity_kg numeric(12,3) not null,
  status text not null default 'pending' check (status in ('pending','approved','rejected','completed')),
  created_at timestamptz default now()
);

create table if not exists invoices (
  id bigint generated always as identity primary key,
  customer_id bigint references customers(id),
  total numeric(12,2) not null default 0,
  discount numeric(12,2) not null default 0,
  created_at timestamptz default now()
);

create table if not exists invoice_items (
  id bigint generated always as identity primary key,
  invoice_id bigint references invoices(id) on delete cascade,
  product_id bigint references products(id),
  pieces int,
  weight_kg numeric(12,3) not null,
  rate numeric(10,2) not null,
  amount numeric(12,2) not null
);

-- Ledger: balance = sum(invoices.total) - sum(payments.amount)
create table if not exists payments (
  id bigint generated always as identity primary key,
  customer_id bigint references customers(id),
  invoice_id bigint references invoices(id),
  amount numeric(12,2) not null,
  paid_at timestamptz default now()
);

-- Sample products
insert into products (name, category, size_label, grade, price_per_kg, stock_pieces, stock_kg) values
  ('Rebar 12mm', 'rebar', '12 mm x 12 m', 'Grade 60', 260, 100, 1065.6),
  ('MS Plate 10mm', 'plate', '2440x1220x10', 'A36', 280, 10, 2336.8),
  ('GI Pipe 48.3', 'pipe', '48.3x3.2 x 6 m', 'ASTM A53', 310, 50, 1068);

-- Security: turn on Row Level Security
alter table profiles enable row level security;
alter table products enable row level security;
alter table inward_stock enable row level security;
alter table cutting_jobs enable row level security;
alter table leftovers enable row level security;
alter table scrap enable row level security;
alter table customers enable row level security;
alter table orders enable row level security;
alter table invoices enable row level security;
alter table invoice_items enable row level security;
alter table payments enable row level security;

create or replace function is_staff() returns boolean
language sql security definer set search_path = public as $$
  select exists (select 1 from profiles where id = auth.uid() and role in ('admin','staff'));
$$;

-- Everyone logged in can see the catalog; only staff can change it
create policy "catalog read" on products for select to authenticated using (true);
create policy "staff manage products" on products for all to authenticated using (is_staff()) with check (is_staff());

-- Staff-only tables
create policy "staff inward" on inward_stock for all to authenticated using (is_staff()) with check (is_staff());
create policy "staff cutting" on cutting_jobs for all to authenticated using (is_staff()) with check (is_staff());
create policy "staff leftovers" on leftovers for all to authenticated using (is_staff()) with check (is_staff());
create policy "staff scrap" on scrap for all to authenticated using (is_staff()) with check (is_staff());
create policy "staff invoices" on invoices for all to authenticated using (is_staff()) with check (is_staff());
create policy "staff invoice items" on invoice_items for all to authenticated using (is_staff()) with check (is_staff());
create policy "staff payments" on payments for all to authenticated using (is_staff()) with check (is_staff());
create policy "staff customers" on customers for all to authenticated using (is_staff()) with check (is_staff());

-- Customers: own profile, own customer row, own orders
create policy "own profile" on profiles for select to authenticated using (id = auth.uid() or is_staff());
create policy "own profile insert" on profiles for insert to authenticated with check (id = auth.uid() and role = 'customer');
create policy "customer sees self" on customers for select to authenticated using (user_id = auth.uid());
create policy "customer own orders read" on orders for select to authenticated
  using (customer_id in (select id from customers where user_id = auth.uid()) or is_staff());
create policy "customer place order" on orders for insert to authenticated
  with check (customer_id in (select id from customers where user_id = auth.uid()));
create policy "staff update orders" on orders for update to authenticated using (is_staff());
