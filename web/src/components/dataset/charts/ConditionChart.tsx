import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts"
import { CONDITION_CHART_COLORS } from "@/lib/chartTheme"

interface Props {
  data: Array<{ name: string; count: number; key: string }>
}

export function ConditionChart({ data }: Props) {
  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart data={data} layout="vertical" margin={{ left: 0, right: 16, top: 4, bottom: 4 }}>
        <XAxis type="number" tick={{ fontSize: 12 }} stroke="var(--color-muted-foreground)" axisLine={false} tickLine={false} />
        <YAxis
          dataKey="name"
          type="category"
          width={90}
          tick={{ fontSize: 12 }}
          stroke="var(--color-muted-foreground)"
          axisLine={false}
          tickLine={false}
        />
        <Tooltip
          contentStyle={{
            background: "var(--color-card)",
            border: "1px solid var(--color-border)",
            borderRadius: "8px",
            fontSize: "13px",
            boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
          }}
        />
        <Bar dataKey="count" radius={[0, 6, 6, 0]} barSize={18}>
          {data.map((entry) => (
            <Cell key={entry.key} fill={CONDITION_CHART_COLORS[entry.key] ?? "var(--color-primary)"} fillOpacity={0.85} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}
