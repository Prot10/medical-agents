import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts"

interface Props {
  data: Array<{ range: string; count: number }>
}

export function AgeHistogram({ data }: Props) {
  return (
    <ResponsiveContainer width="100%" height={220}>
      <BarChart data={data} margin={{ left: 0, right: 8, top: 4, bottom: 4 }}>
        <XAxis
          dataKey="range"
          tick={{ fontSize: 12 }}
          stroke="var(--color-muted-foreground)"
          axisLine={false}
          tickLine={false}
        />
        <YAxis
          tick={{ fontSize: 12 }}
          stroke="var(--color-muted-foreground)"
          axisLine={false}
          tickLine={false}
          allowDecimals={false}
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
        <Bar dataKey="count" fill="var(--color-primary)" radius={[6, 6, 0, 0]} barSize={32} fillOpacity={0.8} />
      </BarChart>
    </ResponsiveContainer>
  )
}
