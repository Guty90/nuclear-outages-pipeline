export default function TableHeader({ columns }) {
  return (
    <thead>
      <tr className="border-b border-neutral-800">
        {columns.map(col => (
          <th
            key={col.key}
            className="px-4 py-3 text-left text-xs uppercase tracking-widest text-neutral-500 font-medium"
          >
            {col.label}
          </th>
        ))}
      </tr>
    </thead>
  )
}