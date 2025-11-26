# DocChat Frontend

React frontend for DocChat - Upload documents and chat with them using AI.

## Features

- 📤 Drag-and-drop PDF upload
- 💬 Real-time chat interface
- 🎨 Modern UI with TailwindCSS
- 📱 Responsive design

## Setup

1. Install dependencies:
```bash
npm install
```

2. Run development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## Project Structure

```
src/
├── components/
│   ├── FileUpload.jsx    # Drag-and-drop upload component
│   └── ChatInterface.jsx  # Chat UI component
├── App.jsx                # Main app component
└── index.css              # Tailwind CSS imports
```

## TODO

- [ ] Connect to FastAPI backend
- [ ] Implement actual file upload to GCS
- [ ] Add user authentication
- [ ] Add loading states and error handling
- [ ] Add citation display for responses
- [ ] Add conversation history persistence

## Technologies

- React 18
- Vite
- TailwindCSS
- Lucide React (icons)
