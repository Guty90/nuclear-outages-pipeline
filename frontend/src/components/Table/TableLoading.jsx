import { Loader2 } from "lucide-react"

export default function TableLoading() {
  return (
    <div className="flex items-center justify-center h-64 text-neutral-500">
      <div className="flex flex-col items-center gap-3">
        <Loader2 className="w-8 h-8 animate-spin text-white" />
        <span className="text-sm uppercase tracking-widest">Loading data...</span>
      </div>
    </div>
  )
}