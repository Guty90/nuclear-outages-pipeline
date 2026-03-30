import { AlertCircle } from "lucide-react"

export default function TableError({ message }) {
  return (
    <div className="flex items-center justify-center h-64">
      <div className="flex flex-col items-center gap-3 text-center">
        <AlertCircle className="w-8 h-8 text-red-400" />
        <span className="text-red-400 text-sm uppercase tracking-widest">Error</span>
        <span className="text-neutral-400 text-sm max-w-md">{message}</span>
      </div>
    </div>
  )
}