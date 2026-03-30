export default function Pagination({ page, limit, total, onPageChange }) {
  const totalPages = Math.ceil(total / limit)
  if (totalPages <= 1) return null

  const pages = []
  const start = Math.max(1, page - 2)
  const end   = Math.min(totalPages, page + 2)

  for (let i = start; i <= end; i++) pages.push(i)

  return (
    <div className="flex items-center justify-between px-4 py-3 border-t border-neutral-800">
      <span className="text-xs text-neutral-500">
        {total.toLocaleString()} total records · Page {page} of {totalPages}
      </span>

      <div className="flex items-center gap-1">
        <button
          onClick={() => onPageChange(page - 1)}
          disabled={page === 1}
          className="px-3 py-1 text-xs text-neutral-400 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors uppercase tracking-widest"
        >
          Prev
        </button>

        {pages.map(p => (
          <button
            key={p}
            onClick={() => onPageChange(p)}
            className={`w-8 h-8 text-xs font-mono transition-colors ${
              p === page
                ? "bg-white text-[#262626] font-bold"
                : "text-neutral-400 hover:text-white"
            }`}
          >
            {p}
          </button>
        ))}

        <button
          onClick={() => onPageChange(page + 1)}
          disabled={page === totalPages}
          className="px-3 py-1 text-xs text-neutral-400 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors uppercase tracking-widest"
        >
          Next
        </button>
      </div>
    </div>
  )
}