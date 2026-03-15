import { PieChart, Pie, Cell, ResponsiveContainer } from "recharts"
import { DIFFICULTY_COLORS } from "@/lib/chartTheme"
import { DifficultyStars } from "@/components/ui/DifficultyStars"

interface Props {
  data: Array<{ name: string; value: number; key: string }>
}

export function DifficultyDonut({ data }: Props) {
  const total = data.reduce((s, d) => s + d.value, 0)

  return (
    <div className="flex items-center gap-6">
      <ResponsiveContainer width="50%" height={220}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={55}
            outerRadius={85}
            paddingAngle={3}
            dataKey="value"
            strokeWidth={0}
          >
            {data.map((entry) => (
              <Cell key={entry.key} fill={DIFFICULTY_COLORS[entry.key as keyof typeof DIFFICULTY_COLORS] ?? "#888"} />
            ))}
          </Pie>
        </PieChart>
      </ResponsiveContainer>
      <div className="space-y-3 flex-1">
        {data.map((d) => {
          const pct = total > 0 ? Math.round((d.value / total) * 100) : 0
          return (
            <div key={d.key} className="flex items-center gap-3">
              <DifficultyStars difficulty={d.key} size="md" />
              <div className="flex-1 min-w-0">
                <div className="text-base font-medium">{d.name}</div>
                <div className="text-sm text-muted-foreground">{d.value} cases</div>
              </div>
              <div className="text-lg font-bold tabular-nums">{pct}%</div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
