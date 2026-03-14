import { LabResultsTable } from "./LabResultsTable"
import { MRIFindings } from "./MRIFindings"
import { ECGReport } from "./ECGReport"
import { EEGReport } from "./EEGReport"
import { CSFResults } from "./CSFResults"
import { LiteratureResults } from "./LiteratureResults"
import { DrugInteractions } from "./DrugInteractions"
import { GenericResult } from "./GenericResult"

interface Props {
  toolName: string
  result: Record<string, unknown>
}

export function ToolResultRenderer({ toolName, result }: Props) {
  // The result wrapper has { tool_name, success, output, error_message }
  const output = (result.output as Record<string, unknown>) ?? result

  if (!result.success) {
    return (
      <div className="text-xs text-red-400 italic">
        {(result.error_message as string) ?? "Tool execution failed"}
      </div>
    )
  }

  switch (toolName) {
    case "interpret_labs":
      return <LabResultsTable data={output} />
    case "analyze_brain_mri":
      return <MRIFindings data={output} />
    case "analyze_ecg":
      return <ECGReport data={output} />
    case "analyze_eeg":
      return <EEGReport data={output} />
    case "analyze_csf":
      return <CSFResults data={output} />
    case "search_medical_literature":
      return <LiteratureResults data={output} />
    case "check_drug_interactions":
      return <DrugInteractions data={output} />
    default:
      return <GenericResult data={output} />
  }
}
