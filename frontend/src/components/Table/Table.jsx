import { getColumns }  from "./tableColumns"
import TableHeader     from "./TableHeader"
import TableRow        from "./TableRow"
import TableLoading    from "./TableLoading"
import TableError      from "./TableError"
import TableEmpty      from "./TableEmpty"

export default function Table({ data, loading, error, dataType, facilities }) {
  const columns = getColumns(dataType)

  if (loading) return <TableLoading />
  if (error)   return <TableError message={error} />
  if (!data.length) return <TableEmpty />

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <TableHeader columns={columns} />
        <tbody>
          {data.map((row, i) => (
            <TableRow key={i} row={row} columns={columns} facilities={facilities} />
          ))}
        </tbody>
      </table>
    </div>
  )
}