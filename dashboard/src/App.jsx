import { motion, AnimatePresence } from 'framer-motion'
import { useSimulation } from './hooks/useSimulation'
import { TopNav } from './components/TopNav'
import { SystemFlow } from './components/SystemFlow'
import { AuthPanel } from './components/AuthPanel'
import { GatewayPanel } from './components/GatewayPanel'
import { FirewallPanel } from './components/FirewallPanel'
import { VehiclePanel } from './components/VehiclePanel'
import { CanInspector } from './components/CanInspector'
import { ThreatCenter } from './components/ThreatCenter'
import { AttackMap } from './components/AttackMap'
import { DefensePanel } from './components/DefensePanel'
import { EventLog } from './components/EventLog'
import { TrustPanel } from './components/TrustPanel'
import { DemoController } from './components/DemoController'

export default function App() {
  const { state, profiles, connected, alert, demoStep, shake, api, runAttack } = useSimulation()

  const presentationMode = state?.settings?.presentation_mode
  const privacyMode = state?.settings?.privacy_mode
  const demoRunning = demoStep?.action && demoStep.action !== 'complete' && demoStep.step >= 0

  const handleAuth = async (step) => {
    if (step === 'connect') await api.connect()
    if (step === 'challenge') await api.challenge()
    if (step === 'sign') {
      await api.sign()
      await api.enableControls()
    }
  }

  const handleRead = (op) => api.request(op)

  if (!state) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#0a0a0a]">
        <motion.p animate={{ opacity: [0.4, 1, 0.4] }} transition={{ repeat: Infinity, duration: 1.5 }} className="text-gray-500">
          Connecting to simulation backend…
        </motion.p>
      </div>
    )
  }

  return (
    <div className={`min-h-screen bg-[#0a0a0a] ${presentationMode ? 'presentation-mode' : ''} ${shake ? 'animate-[shake_0.5s_ease-in-out]' : ''}`}>
      <style>{`
        @keyframes shake {
          0%, 100% { transform: translateX(0); }
          20% { transform: translateX(-6px); }
          40% { transform: translateX(6px); }
          60% { transform: translateX(-4px); }
          80% { transform: translateX(4px); }
        }
      `}</style>

      <TopNav
        state={state}
        profiles={profiles}
        connected={connected}
        presentationMode={presentationMode}
        privacyMode={privacyMode}
        onProfile={(id) => api.setProfile(id)}
        onSettings={(s) => api.settings(s)}
        onRunDemo={() => api.runDemo()}
      />

      <main className="p-4 max-w-[1920px] mx-auto space-y-4">
        <SystemFlow flow={state.flow} presentationMode={presentationMode} />

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
          <div className="lg:col-span-3 space-y-4">
            <AuthPanel auth={state.auth} api={api} onAuth={handleAuth} />
            <GatewayPanel gateway={state.gateway} lockdown={state.gateway?.lockdown} />
            <TrustPanel />
          </div>

          <div className="lg:col-span-6 space-y-4">
            <VehiclePanel vehicle={state.vehicle} api={api} />
            <CanInspector frames={state.can_frames} profileLabel={state.vehicle?.profile_label} />
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FirewallPanel firewall={state.firewall} onRead={handleRead} />
              <DefensePanel defense={state.defense} />
            </div>
            <AttackMap flow={state.flow} />
          </div>

          <div className="lg:col-span-3 space-y-4">
            <ThreatCenter onAttack={runAttack} />
            <DemoController
              onRun={() => api.runDemo()}
              onReset={() => api.resetDemo()}
              demoStep={demoStep}
              running={demoRunning}
            />
            <EventLog events={state.events} privacyMode={privacyMode} />
          </div>
        </div>
      </main>

      <AnimatePresence>
        {alert?.alert && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0 }}
            className={`fixed inset-0 z-50 flex items-center justify-center pointer-events-none ${alert.fullscreen ? 'bg-red-950/80' : ''}`}
          >
            <div className={`px-8 py-6 rounded-2xl border-2 text-center glow-red ${
              alert.alert_color === 'green' ? 'border-green-500 bg-green-950/90' :
              alert.alert_color === 'yellow' ? 'border-yellow-500 bg-yellow-950/90' :
              'border-red-500 bg-red-950/90'
            } ${presentationMode ? 'text-2xl' : 'text-lg'}`}>
              <p className="font-bold tracking-wider">{alert.alert}</p>
              {alert.detail && <p className="text-sm text-gray-300 mt-2 font-mono">{alert.detail}</p>}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
