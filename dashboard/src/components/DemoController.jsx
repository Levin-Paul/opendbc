import { Clapperboard } from 'lucide-react'
import { Panel, Btn } from './ui/Panel'

const STEPS = [
  'Unauthorized connection',
  'Blocked',
  'Valid user connects',
  'Authentication success',
  'Read RPM',
  'Replay attack',
  'Spoofing attempt',
  'CAN injection',
  'ECU flash attempt',
  'Tampering alert',
  'Defense successful',
]

export function DemoController({ onRun, onReset, demoStep, running }) {
  return (
    <Panel title="Demo Scenario Controller" icon={Clapperboard} accent="purple">
      <div className="flex gap-2 mb-3">
        <Btn variant="purple" onClick={onRun} disabled={running}>RUN FULL DEMO</Btn>
        <Btn variant="ghost" onClick={onReset}>RESET DEMO</Btn>
      </div>
      <ol className="text-[11px] space-y-1 text-gray-400">
        {STEPS.map((s, i) => (
          <li
            key={s}
            className={demoStep?.step === i ? 'text-purple-400 font-semibold' : demoStep?.step > i ? 'text-green-600 line-through' : ''}
          >
            {i + 1}. {s}
          </li>
        ))}
      </ol>
      {demoStep?.action === 'complete' && (
        <p className="text-green-400 text-xs mt-2">✓ Full demo sequence complete</p>
      )}
    </Panel>
  )
}
