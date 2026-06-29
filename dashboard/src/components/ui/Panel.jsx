export function Panel({ title, icon: Icon, children, className = '', accent }) {
  const accentClass =
    accent === 'green' ? 'border-green-500/30' :
    accent === 'red' ? 'border-red-500/30' :
    accent === 'blue' ? 'border-blue-500/30' :
    accent === 'purple' ? 'border-purple-500/30' : 'border-[#2a2a2a]'

  return (
    <section className={`panel p-4 border ${accentClass} ${className}`}>
      {title && (
        <header className="flex items-center gap-2 mb-3">
          {Icon && <Icon className="w-4 h-4 text-gray-400" />}
          <h2 className="text-sm font-semibold tracking-wide text-gray-200 uppercase">{title}</h2>
        </header>
      )}
      {children}
    </section>
  )
}

export function Badge({ children, color = 'gray' }) {
  const colors = {
    green: 'bg-green-500/15 text-green-400 border-green-500/40',
    red: 'bg-red-500/15 text-red-400 border-red-500/40',
    yellow: 'bg-yellow-500/15 text-yellow-400 border-yellow-500/40',
    blue: 'bg-blue-500/15 text-blue-400 border-blue-500/40',
    purple: 'bg-purple-500/15 text-purple-400 border-purple-500/40',
    gray: 'bg-gray-500/15 text-gray-400 border-gray-500/40',
  }
  return (
    <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${colors[color] || colors.gray}`}>
      {children}
    </span>
  )
}

export function Btn({ children, onClick, variant = 'default', disabled, className = '' }) {
  const v = {
    default: 'bg-[#252525] hover:bg-[#303030] border-[#333]',
    primary: 'bg-blue-600/80 hover:bg-blue-500 border-blue-500/50',
    danger: 'bg-red-600/80 hover:bg-red-500 border-red-500/50',
    purple: 'bg-purple-600/80 hover:bg-purple-500 border-purple-500/50',
    ghost: 'bg-transparent hover:bg-white/5 border-[#333]',
  }
  return (
    <button
      type="button"
      disabled={disabled}
      onClick={onClick}
      className={`text-xs px-3 py-1.5 rounded-lg border transition ${v[variant]} disabled:opacity-40 ${className}`}
    >
      {children}
    </button>
  )
}
