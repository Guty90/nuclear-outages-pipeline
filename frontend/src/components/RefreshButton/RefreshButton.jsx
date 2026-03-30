import { RefreshCw } from "lucide-react"

export default function RefreshButton({ onClick, loading }) {
  return (
    <button
      onClick={onClick}
      disabled={loading}
      className="flex items-center gap-2 px-4 py-2 bg-white text-[#262626] text-sm font-semibold hover:bg-neutral-200 transition-colors disabled:opacity-40 disabled:cursor-not-allowed tracking-widest uppercase"
    >
      <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
      {loading ? "Refreshing..." : "Refresh Data"}
    </button>
  )
}