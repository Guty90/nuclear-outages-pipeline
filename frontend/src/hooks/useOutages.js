import { useState, useEffect, useCallback } from "react"
import { fetchOutages, fetchFacilities, triggerRefresh } from "../services/api"

export function useOutages() {
  const [data,       setData]       = useState([])
  const [facilities, setFacilities] = useState([])
  const [total,      setTotal]      = useState(0)
  const [loading,    setLoading]    = useState(false)
  const [refreshing, setRefreshing] = useState(false)
  const [error,      setError]      = useState(null)

  const [filters, setFilters] = useState({
    dataType:   "facility",
    page:       1,
    limit:      50,
    facilityId: "",
    startDate:  "",
    endDate:    "",
  })

  const loadFacilities = useCallback(async () => {
    try {
      const res = await fetchFacilities()
      setFacilities(res.data || [])
    } catch (err) {
      console.error("Failed to load facilities:", err)
    }
  }, [])

  const loadData = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await fetchOutages(filters)
      setData(res.data   || [])
      setTotal(res.total || 0)
    } catch (err) {
      setError(err.message)
      setData([])
    } finally {
      setLoading(false)
    }
  }, [filters])

  const refresh = useCallback(async () => {
    setRefreshing(true)
    setError(null)
    try {
      await triggerRefresh()
      await loadData()
    } catch (err) {
      setError(err.message)
    } finally {
      setRefreshing(false)
    }
  }, [loadData])

  const updateFilter = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value, page: 1 }))
  }

  const setPage = (page) => {
    setFilters(prev => ({ ...prev, page }))
  }

  useEffect(() => { loadFacilities() }, [loadFacilities])
  useEffect(() => { loadData() },      [loadData])

  return {
    data, facilities, total, loading, refreshing, error,
    filters, updateFilter, setPage, refresh,
  }
}