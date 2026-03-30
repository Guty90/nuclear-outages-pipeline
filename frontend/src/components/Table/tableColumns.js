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

export const SUMMARY_COLS = [
  { key: "facility_id",         label: "ID" },
  { key: "facility_name",       label: "Facility" },
  { key: "avg_capacity_factor", label: "Avg Capacity Factor (%)" },
  { key: "avg_percent_outage",  label: "Avg Outage (%)" },
  { key: "max_percent_outage",  label: "Max Outage (%)" },
  { key: "total_mw_lost",       label: "Total MW Lost" },
  { key: "days_with_outage",    label: "Days w/ Outage" },
  { key: "last_reported",       label: "Last Reported" },
  { key: "is_active",           label: "Status" },
]

export const SEASONALITY_COLS = [
  { key: "month",              label: "Month" },
  { key: "avg_percent_outage", label: "Avg Outage (%)" },
  { key: "avg_mw_offline",     label: "Avg MW Offline" },
  { key: "total_mw_lost",      label: "Total MW Lost" },
  { key: "record_count",       label: "Records" },
]

export const US_TOTAL_COLS = [
  { key: "period",            label: "Date" },
  { key: "total_capacity",    label: "Total Capacity (MW)" },
  { key: "total_mw_offline",  label: "Total Offline (MW)" },
  { key: "percent_offline",   label: "% Offline" },
  { key: "active_facilities", label: "Active Facilities" },
]

export function getColumns(dataType) {
  if (dataType === "generator")  return GENERATOR_COLS
  if (dataType === "facilities") return FACILITIES_COLS
  if (dataType === "summary")     return SUMMARY_COLS      
  if (dataType === "seasonality") return SEASONALITY_COLS  
  if (dataType === "us_total")    return US_TOTAL_COLS     
  return FACILITY_COLS
}

export function formatValue(key, value) {
  if (value === null || value === undefined) return "—"
  if (["capacity", "outage", "total_mw_lost", "avg_mw_offline", "total_capacity", "total_mw_offline", "record_count", "days_with_outage", "active_facilities"].includes(key))
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