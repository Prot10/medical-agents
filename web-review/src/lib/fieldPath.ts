/**
 * Whether an annotation's `field_path` (e.g. `ground_truth.red_herrings[0]`) still names a
 * field of the case. Annotations written against an earlier case schema can point to fields
 * that no longer exist; the sidebar flags those instead of silently losing them.
 */
export function fieldExists(root: unknown, path: string): boolean {
  let node: unknown = root
  for (const token of path.match(/[^.[\]]+|\[\d+\]/g) ?? []) {
    if (token.startsWith("[")) {
      const index = Number(token.slice(1, -1))
      if (!Array.isArray(node) || index >= node.length) return false
      node = node[index]
    } else {
      if (node === null || typeof node !== "object" || Array.isArray(node)) return false
      if (!Object.prototype.hasOwnProperty.call(node, token)) return false
      node = (node as Record<string, unknown>)[token]
    }
  }
  return true
}
