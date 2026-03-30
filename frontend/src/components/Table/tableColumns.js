export const FACILITY_COLS = [
  { key: "period",         label: "Date" },
  { key: "facility_id",    label: "ID" },
  { key: "facility_name",  label: "Facility" },
  { key: "capacity",       label: "Capacity (MW)" },
  { key: "outage",         label: "Outage (MW)" },
  { key: "percent_outage", label: "% Outage" },
]

export const GENERATOR_COLS = [
  { key: "period",         label: "Date" },
  { key: "facility_id",    label: "Facility ID" },
  { key: "generator_id",   label: "Generator" },
  { key: "capacity",       label: "Capacity (MW)" },
  { key: "outage",         label: "Outage (MW)" },
  { key: "percent_outage", label: "% Outage" },
]

export const FACILITIES_COLS = [
  { key: "facility_id",   label: "ID" },
  { key: "facility_name", label: "Facility Name" },
]

export function getColumns(dataType) {
  if (dataType === "generator")  return GENERATOR_COLS
  if (dataType === "facilities") return FACILITIES_COLS
  return FACILITY_COLS
}

export function formatValue(key, value) {
  if (value === null || value === undefined) return "—"
  if (["capacity", "outage"].includes(key))
    return Number(value).toLocaleString("en-US", { maximumFractionDigits: 1 })
  if (key === "percent_outage")
    return `${Number(value).toFixed(2)}%`
  return value
}

export function getOutageColor(value) {
  const pct = Number(value)
  if (pct === 0)  return "text-emerald-400"
  if (pct < 25)   return "text-yellow-400"
  if (pct < 75)   return "text-orange-400"
  return "text-red-400"
}