-- MAC-Lab internal console schema for Supabase.
-- Run this in Supabase SQL Editor after creating the project.
-- Replace OWNER_EMAIL at the bottom with Professor Sun's login email.

create extension if not exists pgcrypto;

do $$
begin
  create type public.console_role as enum ('owner', 'admin', 'student');
exception when duplicate_object then null;
end $$;

do $$
begin
  create type public.account_status as enum ('pending', 'active', 'suspended');
exception when duplicate_object then null;
end $$;

do $$
begin
  create type public.review_status as enum ('draft', 'submitted', 'review', 'approved', 'public_ready', 'private', 'archived');
exception when duplicate_object then null;
end $$;

do $$
begin
  create type public.page_visibility as enum ('draft', 'published', 'hidden');
exception when duplicate_object then null;
end $$;

create or replace function public.touch_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  email text unique,
  full_name text,
  github_username text,
  avatar_url text,
  role public.console_role not null default 'student',
  status public.account_status not null default 'pending',
  homepage_slug text unique,
  bio_zh text,
  bio_en text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.student_pages (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references public.profiles(id) on delete cascade,
  title_zh text not null,
  title_en text,
  slug text unique,
  research_tags text[] not null default '{}',
  body_zh text,
  body_en text,
  publications jsonb not null default '[]'::jsonb,
  projects jsonb not null default '[]'::jsonb,
  achievements jsonb not null default '[]'::jsonb,
  visibility public.page_visibility not null default 'draft',
  reviewed_by uuid references public.profiles(id),
  published_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint student_pages_one_per_owner unique (owner_id)
);

create table if not exists public.lab_news (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  category text not null default 'lab',
  summary text,
  source_url text,
  body text,
  status public.review_status not null default 'submitted',
  submitted_by uuid references public.profiles(id),
  reviewed_by uuid references public.profiles(id),
  public_url text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.lab_outputs (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  type text not null default 'project',
  summary text,
  status public.review_status not null default 'draft',
  submitted_by uuid references public.profiles(id),
  owner_id uuid references public.profiles(id),
  public_url text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.partner_requests (
  id uuid primary key default gen_random_uuid(),
  organization text not null,
  contact_name text,
  contact_email text,
  scenario text,
  need_summary text,
  status public.review_status not null default 'submitted',
  owner_id uuid references public.profiles(id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create or replace function public.current_console_role()
returns text
language sql
stable
security definer
set search_path = public
as $$
  select role::text
  from public.profiles
  where id = auth.uid()
    and status = 'active'
  limit 1;
$$;

create or replace function public.is_console_admin()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select coalesce(public.current_console_role() in ('owner', 'admin'), false);
$$;

create or replace function public.is_console_owner()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select coalesce(public.current_console_role() = 'owner', false);
$$;

create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.profiles (id, email, full_name, github_username, avatar_url)
  values (
    new.id,
    new.email,
    coalesce(new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'name'),
    new.raw_user_meta_data->>'user_name',
    new.raw_user_meta_data->>'avatar_url'
  )
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

drop trigger if exists profiles_touch_updated_at on public.profiles;
create trigger profiles_touch_updated_at
  before update on public.profiles
  for each row execute function public.touch_updated_at();

drop trigger if exists student_pages_touch_updated_at on public.student_pages;
create trigger student_pages_touch_updated_at
  before update on public.student_pages
  for each row execute function public.touch_updated_at();

drop trigger if exists lab_news_touch_updated_at on public.lab_news;
create trigger lab_news_touch_updated_at
  before update on public.lab_news
  for each row execute function public.touch_updated_at();

drop trigger if exists lab_outputs_touch_updated_at on public.lab_outputs;
create trigger lab_outputs_touch_updated_at
  before update on public.lab_outputs
  for each row execute function public.touch_updated_at();

drop trigger if exists partner_requests_touch_updated_at on public.partner_requests;
create trigger partner_requests_touch_updated_at
  before update on public.partner_requests
  for each row execute function public.touch_updated_at();

alter table public.profiles enable row level security;
alter table public.student_pages enable row level security;
alter table public.lab_news enable row level security;
alter table public.lab_outputs enable row level security;
alter table public.partner_requests enable row level security;

drop policy if exists "profiles_select_self_or_admin" on public.profiles;
create policy "profiles_select_self_or_admin"
  on public.profiles for select
  using (id = auth.uid() or public.is_console_admin());

drop policy if exists "profiles_owner_updates_roles" on public.profiles;
create policy "profiles_owner_updates_roles"
  on public.profiles for update
  using (public.is_console_owner())
  with check (public.is_console_owner());

drop policy if exists "student_pages_select_scope" on public.student_pages;
create policy "student_pages_select_scope"
  on public.student_pages for select
  using (owner_id = auth.uid() or public.is_console_admin());

drop policy if exists "student_pages_insert_own" on public.student_pages;
create policy "student_pages_insert_own"
  on public.student_pages for insert
  with check (owner_id = auth.uid() and public.current_console_role() is not null);

drop policy if exists "student_pages_update_own_or_admin" on public.student_pages;
create policy "student_pages_update_own_or_admin"
  on public.student_pages for update
  using (owner_id = auth.uid() or public.is_console_admin())
  with check ((owner_id = auth.uid() and public.current_console_role() is not null) or public.is_console_admin());

drop policy if exists "lab_news_select_scope" on public.lab_news;
create policy "lab_news_select_scope"
  on public.lab_news for select
  using (submitted_by = auth.uid() or public.is_console_admin());

drop policy if exists "lab_news_insert_authenticated" on public.lab_news;
create policy "lab_news_insert_authenticated"
  on public.lab_news for insert
  with check (public.current_console_role() is not null and submitted_by = auth.uid());

drop policy if exists "lab_news_update_admin" on public.lab_news;
create policy "lab_news_update_admin"
  on public.lab_news for update
  using (public.is_console_admin())
  with check (public.is_console_admin());

drop policy if exists "lab_outputs_select_scope" on public.lab_outputs;
create policy "lab_outputs_select_scope"
  on public.lab_outputs for select
  using (submitted_by = auth.uid() or owner_id = auth.uid() or public.is_console_admin());

drop policy if exists "lab_outputs_insert_authenticated" on public.lab_outputs;
create policy "lab_outputs_insert_authenticated"
  on public.lab_outputs for insert
  with check (public.current_console_role() is not null and submitted_by = auth.uid());

drop policy if exists "lab_outputs_update_scope" on public.lab_outputs;
create policy "lab_outputs_update_scope"
  on public.lab_outputs for update
  using (submitted_by = auth.uid() or owner_id = auth.uid() or public.is_console_admin())
  with check (((submitted_by = auth.uid() or owner_id = auth.uid()) and public.current_console_role() is not null) or public.is_console_admin());

drop policy if exists "partner_requests_select_admin" on public.partner_requests;
create policy "partner_requests_select_admin"
  on public.partner_requests for select
  using (public.is_console_admin());

drop policy if exists "partner_requests_insert_authenticated" on public.partner_requests;
create policy "partner_requests_insert_authenticated"
  on public.partner_requests for insert
  with check (public.current_console_role() is not null);

drop policy if exists "partner_requests_update_admin" on public.partner_requests;
create policy "partner_requests_update_admin"
  on public.partner_requests for update
  using (public.is_console_admin())
  with check (public.is_console_admin());

grant usage on schema public to anon, authenticated;
grant select, insert, update on public.profiles to authenticated;
grant select, insert, update on public.student_pages to authenticated;
grant select, insert, update on public.lab_news to authenticated;
grant select, insert, update on public.lab_outputs to authenticated;
grant select, insert, update on public.partner_requests to authenticated;
grant execute on function public.current_console_role() to authenticated;
grant execute on function public.is_console_admin() to authenticated;
grant execute on function public.is_console_owner() to authenticated;

-- After Professor Sun signs in once, run the following line with the real login email.
-- update public.profiles set role = 'owner', status = 'active' where email = 'OWNER_EMAIL';
