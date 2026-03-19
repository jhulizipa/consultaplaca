import { useState } from 'react'

export default function App() {
  const [placa, setPlaca] = useState('')
  const [resultado, setResultado] = useState(null)
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState(null)

  async function consultar(e) {
    e.preventDefault()
    setCargando(true)
    setError(null)
    setResultado(null)
    try {
      const res = await fetch(`http://localhost:8000/consulta/${placa}`)
      const data = await res.json()
      if (data.error) setError(data.error)
      else setResultado(data)
    } catch {
      setError('No se pudo conectar al servidor.')
    } finally {
      setCargando(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <h1 className="text-3xl font-medium text-center mb-2">ConsultaPlaca</h1>
        <p className="text-gray-500 text-center text-sm mb-8">
          Reporte completo de cualquier vehículo en Colombia
        </p>
        <form onSubmit={consultar} className="flex gap-2 mb-4">
          <input value={placa} onChange={e => setPlaca(e.target.value.toUpperCase())}
            placeholder="ABC123" maxLength={7}
            className="flex-1 px-4 py-3 border rounded-lg font-mono text-lg uppercase tracking-widest" />
          <button disabled={cargando}
            className="px-5 py-3 bg-blue-600 text-white rounded-lg">
            {cargando ? '...' : 'Consultar'}
          </button>
        </form>
        {error && <div className="bg-red-50 text-red-700 rounded-lg p-3 text-sm">{error}</div>}
        {resultado && <div className="bg-white border rounded-xl p-5">
          <div className="text-2xl font-mono font-medium mb-2">{resultado.placa}</div>
          <div className="text-sm text-gray-500">{resultado.mensaje}</div>
        </div>}
      </div>
    </div>
  )
}