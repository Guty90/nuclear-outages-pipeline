import { useOutages }     from "./hooks/useOutages"
import Filters            from "./components/Filters/Filters"
import Table              from "./components/Table/Table"
import Pagination         from "./components/Pagination/Pagination"
import RefreshButton      from "./components/RefreshButton/RefreshButton"

export default function App() {
  const {
    data, facilities, total, loading, refreshing, error,
    filters, updateFilter, setPage, refresh,
  } = useOutages()

  return (
    <div className="min-h-screen bg-[#262626] text-white font-mono">

      {/* Header */}
      <header className="border-b border-neutral-800 px-6 py-4">
        <div className="max-w-screen-xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4">
            <span className="text-xl font-bold tracking-tight">[Λ] Arkham</span>
            <span className="text-neutral-600 text-xs uppercase tracking-widest hidden md:block">
              Nuclear Outages Pipeline
            </span>
          </div>
          <RefreshButton onClick={refresh} loading={refreshing} />
        </div>
      </header>

      {/* Main */}
      <main className="max-w-screen-xl mx-auto px-6 py-6 flex flex-col gap-4">

        {/* Stats bar */}
        <div className="flex items-center gap-6 text-xs text-neutral-500 uppercase tracking-widest">
          <span>
            <span className="text-white font-semibold">
              {total.toLocaleString()}
            </span>{" "}records
          </span>
          <span>
            <span className="text-white font-semibold">
              {facilities.length}
            </span>{" "}facilities
          </span>
          <span>
            Dataset:{" "}
            <span className="text-white font-semibold">
              {filters.dataType}
            </span>
          </span>
        </div>

        {/* Filters */}
        <Filters
          filters={filters}
          facilities={facilities}
          onChange={updateFilter}
        />

        {/* Table */}
        <div className="border border-neutral-800 bg-neutral-950">
          <Table
            data={data}
            loading={loading}
            error={error}
            dataType={filters.dataType}
            facilities={facilities}
          />
          <Pagination
            page={filters.page}
            limit={filters.limit}
            total={total}
            onPageChange={setPage}
          />
        </div>

      </main>

      {/* Footer */}
      <footer className="border-t border-neutral-800 px-6 py-4 mt-8">
        <div className="max-w-screen-xl mx-auto flex items-center justify-between text-xs text-neutral-700">
          <span>Nuclear Outages Pipeline</span>
          <span>EIA Open Data</span>
        </div>
      </footer>

    </div>
  )
}