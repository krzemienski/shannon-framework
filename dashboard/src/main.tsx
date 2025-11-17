import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Decisions } from './panels/Decisions'
import './index.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Decisions />
  </StrictMode>,
)
