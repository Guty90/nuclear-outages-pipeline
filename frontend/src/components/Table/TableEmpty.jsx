import { Database } from "lucide-react"

export default function TableEmpty() {
  return (
    <div className="flex items-center justify-center h-64">
      <div className="flex flex-col items-center gap-3">
        <Database className="w-8 h-8 text-neutral-600" />
        <span className="text-neutral-600 text-sm uppercase tracking-widest">
          No data available
        </span>
        <span className="text-neutral-700 text-xs">
          Try adjusting your filters or refresh the data
        </span>
      </div>
    </div>
  )
}