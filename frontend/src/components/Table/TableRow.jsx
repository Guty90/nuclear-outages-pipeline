import { formatValue, getOutageColor } from "./tableColumns"

export default function TableRow({ row, columns, facilities }) {
  return (
    <tr className="border-b border-neutral-900 hover:bg-neutral-900 transition-colors">
      {columns.map(col => {
        const value = col.key === "facility_name"
        ? facilities?.find(f => f.facility_id === row.facility_id)?.facility_name ?? "—"
        : col.key === "is_active"
            ? row[col.key] ? "Active" : "Inactive"               
        : col.key === "month"
            ? ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][row[col.key] - 1] 
        : row[col.key]

        return (
          <td key={col.key} className="px-4 py-3 text-neutral-300 font-mono text-xs">
            {col.key === "percent_outage" || col.key === "percent_offline" || col.key === "avg_percent_outage" ? (
            <span className={`font-semibold ${getOutageColor(row[col.key])}`}>
                {row[col.key] !== null && row[col.key] !== undefined
                ? `${Number(row[col.key]).toFixed(2)}%`
                : "—"
                }
            </span>
            ) : col.key === "is_active" ? (
            <span className={value === "Active" ? "text-emerald-400 font-semibold" : "text-red-400 font-semibold"}>
                {value}
            </span>
            ) : (
            formatValue(col.key, value)
            )}
          </td>
        )
      })}
    </tr>
  )
}