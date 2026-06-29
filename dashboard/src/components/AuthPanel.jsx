import { Lock, ShieldCheck, HelpCircle } from 'lucide-react'
import { Panel, Badge, Btn } from './ui/Panel'

const TIPS = {
  nonce: 'A one-time random number. Each auth attempt uses a fresh nonce so old signatures cannot be reused.',
  signature: 'The device signs the nonce with its private key. The gateway verifies with the trusted public key.',
  replay: 'Reusing a captured request ID or old challenge fails — the gateway tracks seen IDs and expires challenges.',
}

function Tip({ label, id }) {
  return (
    <span className="inline-flex items-center gap-1 text-[10px] text-gray-500 cursor-help" title={TIPS[id]}>
      <HelpCircle className="w-3 h-3" /> {label}
    </span>
  )
}

export function AuthPanel({ auth, api, onAuth }) {
  const stateColor =
    auth?.state === 'verified' ? 'green' :
    auth?.state === 'blocked' ? 'red' :
    auth?.state === 'authenticating' ? 'yellow' : 'gray'

  return (
    <Panel title="Authentication" icon={Lock} accent={stateColor === 'green' ? 'green' : 'blue'}>
      <div className="space-y-3 text-sm">
        <div className="flex justify-between">
          <span className="text-gray-500">Status</span>
          <Badge color={stateColor}>{auth?.state || 'disconnected'}</Badge>
        </div>
        <div className="flex justify-between font-mono text-xs">
          <span className="text-gray-500">Device ID</span>
          <span>{auth?.device_id || '—'}</span>
        </div>
        <div className="flex justify-between font-mono text-xs break-all">
          <span className="text-gray-500">Nonce</span>
          <span className="text-blue-400 max-w-[140px] truncate">{auth?.nonce_hex || '—'}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-500">Signature</span>
          <span className={auth?.signature_verified ? 'text-green-400' : 'text-gray-500'}>
            {auth?.signature_verified ? '✓ Verified' : 'Pending'}
          </span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-500">Session</span>
          <span>{auth?.session_token_preview || 'Inactive'}</span>
        </div>
        <div className="flex flex-wrap gap-1 pt-1">
          <Tip label="Nonce?" id="nonce" />
          <Tip label="Signature?" id="signature" />
          <Tip label="Replay?" id="replay" />
        </div>
        <div className="flex flex-wrap gap-2 pt-2 border-t border-[#2a2a2a]">
          <Btn onClick={() => onAuth('connect')}>Connect</Btn>
          <Btn variant="primary" onClick={() => onAuth('challenge')}>Request Auth</Btn>
          <Btn variant="primary" onClick={() => onAuth('sign')}>
            <ShieldCheck className="w-3 h-3 inline" /> Sign Challenge
          </Btn>
          <Btn variant="ghost" onClick={() => api.disconnect()}>Disconnect</Btn>
          <Btn variant="danger" onClick={() => api.revoke()}>Revoke</Btn>
        </div>
      </div>
    </Panel>
  )
}
