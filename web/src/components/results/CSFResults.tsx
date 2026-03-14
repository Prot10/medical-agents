export function CSFResults({ data }: { data: Record<string, unknown> }) {
  const appearance = data.appearance as string | undefined
  const pressure = data.opening_pressure as string | number | undefined
  const cellCount = data.cell_count as Record<string, unknown> | undefined
  const protein = data.protein as string | number | undefined
  const glucose = data.glucose as string | number | undefined
  const glucoseRatio = data.glucose_ratio as string | number | undefined
  const specialTests = data.special_tests as Record<string, unknown> | Array<Record<string, unknown>> | undefined
  const interpretation = data.interpretation as string | undefined

  return (
    <div className="space-y-2">
      {/* Key values grid */}
      <div className="grid grid-cols-2 gap-2">
        {appearance && <KV label="Appearance" value={appearance} />}
        {pressure && <KV label="Opening Pressure" value={`${pressure}`} />}
        {protein && <KV label="Protein" value={`${protein}`} />}
        {glucose && <KV label="Glucose" value={`${glucose}`} />}
        {glucoseRatio && <KV label="CSF/Serum Ratio" value={`${glucoseRatio}`} />}
      </div>

      {cellCount && (
        <div>
          <div className="text-[10px] font-semibold text-muted-foreground mb-0.5">Cell Count</div>
          <div className="grid grid-cols-2 gap-1">
            {Object.entries(cellCount).map(([key, val]) => (
              <KV key={key} label={key} value={`${val}`} />
            ))}
          </div>
        </div>
      )}

      {specialTests && (
        <div>
          <div className="text-[10px] font-semibold text-muted-foreground mb-0.5">Special Tests</div>
          {Array.isArray(specialTests) ? (
            <div className="space-y-0.5">
              {specialTests.map((t, i) => (
                <div key={i} className="text-[10px] text-muted-foreground">
                  {Object.entries(t).map(([k, v]) => `${k}: ${v}`).join(", ")}
                </div>
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-2 gap-1">
              {Object.entries(specialTests).map(([key, val]) => (
                <KV key={key} label={key} value={typeof val === 'object' ? JSON.stringify(val) : `${val}`} />
              ))}
            </div>
          )}
        </div>
      )}

      {interpretation && (
        <div className="text-[11px] leading-relaxed">
          <span className="font-semibold text-foreground/80">Interpretation: </span>
          <span className="text-muted-foreground">{interpretation}</span>
        </div>
      )}
    </div>
  )
}

function KV({ label, value }: { label: string; value: string }) {
  return (
    <div className="text-[10px]">
      <span className="font-medium text-foreground/70 capitalize">{label.replace(/_/g, " ")}:</span>{" "}
      <span className="text-muted-foreground font-mono">{value}</span>
    </div>
  )
}
