const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"
const API_KEY  = import.meta.env.VITE_APP_API_KEY || ""

const headers = {
  "X-API-Key": API_KEY,
  "Content-Type": "application/json",
}

export const fetchOutages = async (filters = {}) => {
  const params = new URLSearchParams()

  params.append("type", filters.dataType || "facility")
  params.append("page",      filters.page      || 1)
  params.append("limit",     filters.limit     || 50)

  if (filters.facilityId) params.append("facility_id", filters.facilityId)
  if (filters.startDate)  params.append("start_date",  filters.startDate)
  if (filters.endDate)    params.append("end_date",    filters.endDate)

  const response = await fetch(`${BASE_URL}/data?${params}`, { headers })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || "Failed to fetch data")
  }

  return response.json()
}

export const fetchFacilities = async () => {
  const params = new URLSearchParams()
  params.append("type", "facilities")
  params.append("limit", 100)

  const response = await fetch(`${BASE_URL}/data?${params}`, { headers })

  if (!response.ok) {
    const error = await response.json() 
    throw new Error(error.detail || "Failed to fetch facilities")
  }

  return response.json()
}

export const triggerRefresh = async () => {
  const response = await fetch(`${BASE_URL}/refresh`, { headers })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || "Refresh failed")
  }

  return response.json()
}