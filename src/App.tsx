import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Post from './pages/Post'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/post/:id" element={<Post />} />
    </Routes>
  )
}
