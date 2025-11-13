// Small helper to format park properties into HTML for popups
export function formatParkPopup(props: any): string {
  const name = props.NAME || props.LABEL || props.name || 'Park';
  const address = props.ADDRESS || '';
  const parkCode = props.PARK_CODE || props.PARKCODE || '';
  const source = props.SOURCE || '';

  // Build a simple, safe HTML snippet. Values are escaped via JSON.stringify when embedded.
  const parts: string[] = [];
  parts.push(`<h3>${escapeHtml(name)}</h3>`);
  if (address) parts.push(`<div><strong>Address:</strong> ${escapeHtml(address)}</div>`);
  if (parkCode) parts.push(`<div><strong>Code:</strong> ${escapeHtml(String(parkCode))}</div>`);
  if (source) parts.push(`<div><strong>Source:</strong> ${escapeHtml(source)}</div>`);

  return parts.join('');
}

function escapeHtml(str: string): string {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// Export a default no-op React component so Expo Router doesn't treat this as a missing-route export.
export default function ParkDetails() {
  return null;
}
