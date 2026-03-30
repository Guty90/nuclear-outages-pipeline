export default function Filters({ filters, facilities, onChange }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-3 p-4 bg-neutral-900 border border-neutral-800">

      {/* Data type */}
      <div className="flex flex-col gap-1">
        <label className="text-xs text-neutral-500 uppercase tracking-widest">
          Dataset
        </label>
        <select
          value={filters.dataType}
          onChange={e => onChange("dataType", e.target.value)}
          className="bg-neutral-800 border border-neutral-700 text-white text-sm px-3 py-2 focus:outline-none focus:border-white transition-colors"
        >
          <option value="facility">Facility Outages</option>
          <option value="generator">Generator Outages</option>
          <option value="facilities">Facilities</option>
        </select>
      </div>

      {/* Facility */}
      <div className="flex flex-col gap-1">
        <label className="text-xs text-neutral-500 uppercase tracking-widest">
          Facility
        </label>
        <select
          value={filters.facilityId}
          onChange={e => onChange("facilityId", e.target.value)}
          disabled={filters.dataType === "facilities"}
          className="bg-neutral-800 border border-neutral-700 text-white text-sm px-3 py-2 focus:outline-none focus:border-white transition-colors disabled:opacity-40"
        >
          <option value="">All facilities</option>
          {facilities.map(f => (
            <option key={f.facility_id} value={f.facility_id}>
              {f.facility_name}
            </option>
          ))}
        </select>
      </div>

      {/* Start date */}
      <div className="flex flex-col gap-1">
        <label className="text-xs text-neutral-500 uppercase tracking-widest">
          Start Date
        </label>
        <input
          type="date"
          value={filters.startDate}
          onChange={e => onChange("startDate", e.target.value)}
          disabled={filters.dataType === "facilities"}
          className="bg-neutral-800 border border-neutral-700 text-white text-sm px-3 py-2 focus:outline-none focus:border-white transition-colors disabled:opacity-40"
        />
      </div>

      {/* End date */}
      <div className="flex flex-col gap-1">
        <label className="text-xs text-neutral-500 uppercase tracking-widest">
          End Date
        </label>
        <input
          type="date"
          value={filters.endDate}
          onChange={e => onChange("endDate", e.target.value)}
          disabled={filters.dataType === "facilities"}
          className="bg-neutral-800 border border-neutral-700 text-white text-sm px-3 py-2 focus:outline-none focus:border-white transition-colors disabled:opacity-40"
        />
      </div>

    </div>
  )
}