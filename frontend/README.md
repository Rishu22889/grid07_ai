# Grid07 AI - React + TypeScript Frontend

## Development

```bash
cd frontend
npm install
npm run dev
```

The dev server will start at `http://localhost:5173`

## Build

```bash
npm run build
```

The production build will be in the `dist/` folder.

## Tech Stack

- React 19
- TypeScript 6
- Vite 8
- Oxlint

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Navbar.tsx
│   │   ├── Hero.tsx
│   │   ├── RouterPhase.tsx
│   │   ├── ContentPhase.tsx
│   │   └── CombatPhase.tsx
│   ├── App.tsx
│   ├── App.css
│   ├── main.tsx
│   └── index.css
├── public/
├── package.json
└── vite.config.ts
```

## API Integration

The frontend automatically detects the environment:
- **Development**: `http://localhost:5001/api`
- **Production**: `/api` (Vercel serverless)

## Features

- ✅ Three-phase interactive demo
- ✅ Real-time API integration
- ✅ Fully responsive design
- ✅ TypeScript type safety
- ✅ Component-based architecture
