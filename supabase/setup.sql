-- Supabase SQL: trips table + Relay trigger using pg_net
-- Adjust the RELAY_ENDPOINT placeholder to your Supabase Relay URL

create extension if not exists "pgcrypto";
create extension if not exists pg_net;

create table if not exists public.trips (
  id uuid primary key default gen_random_uuid(),
  session_id text not null,
  user_name text,
  destination text,
  days int,
  travel_style text,
  budget_range text,
  category text,
  complete boolean default false,
  relayed boolean default false,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create or replace function public.touch_updated_at() returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

create trigger trips_touch_updated_at
before insert or update on public.trips
for each row execute function public.touch_updated_at();

-- Relay trigger: fire when record complete, required fields present, and not yet relayed
create or replace function public.relay_trip_if_complete() returns trigger as $$
declare
  payload text;
begin
  -- Only act when record is complete and not already relayed
  if (new.complete is true) and (new.relayed is false) then
    if new.destination is not null and new.days is not null and new.travel_style is not null then
      if new.category in ('itinerary') or (new.category in ('budget','luxury') and new.budget_range is not null) then
        payload := json_build_object(
          'user_name', new.user_name,
          'destination', new.destination,
          'days', new.days,
          'travel_style', new.travel_style,
          'budget_range', new.budget_range,
          'category', new.category
        )::text;

        -- Replace RELAY_ENDPOINT_URL with your Supabase Relay/pg_net-enabled endpoint
        perform pg_net.http_post('https://RELAY_ENDPOINT_URL', payload, 'application/json');

        -- mark as relayed to avoid duplication
        update public.trips set relayed = true where id = new.id and relayed = false;
      end if;
    end if;
  end if;
  return new;
end;
$$ language plpgsql security definer;

create trigger trips_relay_trigger
after insert or update on public.trips
for each row execute function public.relay_trip_if_complete();
