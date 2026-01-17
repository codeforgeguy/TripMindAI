# AI Travel Planner ✈️

An AI-powered conversational travel planning assistant built with
FastAPI, LangGraph, Supabase, and React.

## Features

- Natural language travel planning
- Intent classification (itinerary, budget, luxury)
- Step-by-step clarification (one question at a time)
- Persistent state with Supabase
- Webhook delivery via Supabase Relay (no backend webhooks)
- LLM-assisted intent extraction

## Architecture Highlights

- LangGraph for deterministic conversation flow
- Supabase Postgres triggers for outbound integration
- Clean separation of AI, logic, and infrastructure
- Production-safe webhook handling

## Tech Stack

**Frontend**
- React (Vite)

**Backend**
- FastAPI
- LangGraph
- OpenAI-compatible LLM

**Database**
- Supabase (Postgres + Relay triggers)

## Why This Project Matters

This project demonstrates:
- Real-world AI workflow design
- Event-driven backend architecture
- Safe LLM usage (no hallucinated side effects)
- Production-grade data pipelines

## Future Improvements

- Auth & user sessions
- Multi-trip history
- Maps & itinerary export
- Streaming responses
