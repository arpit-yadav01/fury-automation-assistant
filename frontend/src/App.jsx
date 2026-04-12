// frontend/src/App.jsx
// Fury Dashboard — main app

import { useState, useEffect, useCallback } from "react";
import axios from "axios";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell
} from "recharts";

const API = "http://localhost:8000";

// -------------------------
// COLORS
// -------------------------
const C = {
  purple: "#7F77DD",
  teal:   "#1D9E75",
  amber:  "#BA7517",
  coral:  "#D85A30",
  blue:   "#378ADD",
  green:  "#639922",
  gray:   "#888780",
  red:    "#E24B4A",
};

// -------------------------
// API HOOKS
// -------------------------
function useApi(endpoint, interval = 0) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetch = useCallback(async () => {
    try {
      const res = await axios.get(`${API}${endpoint}`);
      setData(res.data);
    } catch {
      setData(null);
    } finally {
      setLoading(false);
    }
  }, [endpoint]);

  useEffect(() => {
    fetch();
    if (interval > 0) {
      const t = setInterval(fetch, interval);
      return () => clearInterval(t);
    }
  }, [fetch, interval]);

  return { data, loading, refetch: fetch };
}

// -------------------------
// COMPONENTS
// -------------------------

function Card({ title, children, accent }) {
  return (
    <div style={{
      background: "var(--color-background-secondary, #f9f9f7)",
      border: `1px solid var(--color-border-tertiary, rgba(0,0,0,0.1))`,
      borderRadius: 12,
      padding: "16px 20px",
      marginBottom: 16,
      borderLeft: accent ? `3px solid ${accent}` : undefined,
    }}>
      {title && (
        <div style={{
          fontSize: 12, fontWeight: 500, color: C.gray,
          marginBottom: 10, textTransform: "uppercase", letterSpacing: 1
        }}>
          {title}
        </div>
      )}
      {children}
    </div>
  );
}

function Badge({ text, color }) {
  return (
    <span style={{
      background: color + "22",
      color: color,
      border: `1px solid ${color}44`,
      borderRadius: 6,
      padding: "2px 8px",
      fontSize: 11,
      fontWeight: 500,
      marginRight: 4,
    }}>
      {text}
    </span>
  );
}

function Stat({ label, value, color }) {
  return (
    <div style={{ textAlign: "center", padding: "8px 16px" }}>
      <div style={{ fontSize: 28, fontWeight: 500, color: color || C.purple }}>
        {value}
      </div>
      <div style={{ fontSize: 12, color: C.gray, marginTop: 2 }}>{label}</div>
    </div>
  );
}

// -------------------------
// TABS
// -------------------------
const TABS = ["Overview", "History", "Patterns", "Reflections", "Skills", "Knowledge"];

// -------------------------
// OVERVIEW TAB
// -------------------------
function OverviewTab() {
  const { data: status } = useApi("/status", 3000);
  const { data: episodes } = useApi("/episodes", 10000);
  const { data: history } = useApi("/history?limit=5", 5000);

  const successRate = episodes
    ? Math.round((episodes.success_rate || 0) * 100)
    : 0;

  return (
    <div>
      <Card title="Fury Status" accent={C.teal}>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 8 }}>
          <Badge text="RUNNING" color={C.teal} />
          {status?.context?.app && <Badge text={`app: ${status.context.app}`} color={C.blue} />}
          {status?.context?.site && <Badge text={`site: ${status.context.site}`} color={C.amber} />}
          {status?.context?.file && <Badge text={`file: ${status.context.file}`} color={C.purple} />}
        </div>
        <div style={{ fontSize: 12, color: C.gray }}>
          Last updated: {status?.timestamp?.slice(0, 19) || "—"}
        </div>
      </Card>

      <div style={{ display: "flex", gap: 12, marginBottom: 16 }}>
        <Card title="Episodes" style={{ flex: 1 }}>
          <Stat label="Total runs" value={episodes?.total || 0} color={C.purple} />
        </Card>
        <Card>
          <Stat label="Success rate" value={`${successRate}%`} color={successRate > 70 ? C.teal : C.coral} />
        </Card>
        <Card>
          <Stat label="Top action" value={episodes?.top_intents?.[0]?.intent || "—"} color={C.blue} />
        </Card>
      </div>

      <Card title="Recent commands" accent={C.purple}>
        {history?.items?.map((item, i) => (
          <div key={i} style={{
            display: "flex", justifyContent: "space-between",
            alignItems: "center", padding: "6px 0",
            borderBottom: i < history.items.length - 1
              ? "1px solid var(--color-border-tertiary)" : "none"
          }}>
            <div style={{ fontSize: 13, color: "var(--color-text-primary)" }}>
              {item.command}
            </div>
            <div style={{ display: "flex", gap: 6, alignItems: "center" }}>
              {item.actions?.slice(0, 2).map((a, j) => (
                <Badge key={j} text={a} color={C.gray} />
              ))}
              <Badge
                text={item.success ? "ok" : "fail"}
                color={item.success ? C.teal : C.red}
              />
            </div>
          </div>
        ))}
      </Card>
    </div>
  );
}

// -------------------------
// HISTORY TAB
// -------------------------
function HistoryTab() {
  const { data, loading } = useApi("/history?limit=50");

  if (loading) return <div style={{ color: C.gray, padding: 20 }}>Loading...</div>;

  return (
    <div>
      <Card title={`Command history — ${data?.total || 0} total`} accent={C.blue}>
        {data?.items?.map((item, i) => (
          <div key={i} style={{
            padding: "10px 0",
            borderBottom: i < data.items.length - 1
              ? "1px solid var(--color-border-tertiary)" : "none"
          }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
              <div style={{ fontSize: 13, fontWeight: 500 }}>{item.command}</div>
              <Badge
                text={item.success ? "success" : "failed"}
                color={item.success ? C.teal : C.red}
              />
            </div>
            <div style={{ display: "flex", gap: 4, flexWrap: "wrap" }}>
              {item.actions?.map((a, j) => (
                <Badge key={j} text={a} color={C.gray} />
              ))}
            </div>
            <div style={{ fontSize: 11, color: C.gray, marginTop: 4 }}>
              {item.timestamp?.slice(0, 19)}
            </div>
          </div>
        ))}
      </Card>
    </div>
  );
}

// -------------------------
// PATTERNS TAB
// -------------------------
function PatternsTab() {
  const { data, loading } = useApi("/patterns");

  if (loading) return <div style={{ color: C.gray, padding: 20 }}>Analyzing patterns...</div>;

  const topActions = data?.top_actions?.slice(0, 8) || [];

  return (
    <div>
      <Card title="Top actions" accent={C.amber}>
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={topActions}>
            <XAxis dataKey="action" tick={{ fontSize: 11 }} />
            <YAxis tick={{ fontSize: 11 }} />
            <Tooltip />
            <Bar dataKey="count" radius={4}>
              {topActions.map((_, i) => (
                <Cell key={i} fill={Object.values(C)[i % Object.values(C).length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </Card>

      <Card title="Template patterns" accent={C.purple}>
        {data?.templates?.map((t, i) => (
          <div key={i} style={{
            padding: "8px 0",
            borderBottom: i < data.templates.length - 1
              ? "1px solid var(--color-border-tertiary)" : "none"
          }}>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <div style={{ fontSize: 13, fontWeight: 500 }}>{t.template}</div>
              <Badge text={`${t.count}x`} color={C.purple} />
            </div>
            <div style={{ fontSize: 12, color: C.gray, marginTop: 2 }}>
              e.g. "{t.example}"
            </div>
          </div>
        ))}
      </Card>

      <Card title="Failure patterns" accent={C.red}>
        {data?.failures?.length === 0 && (
          <div style={{ color: C.teal, fontSize: 13 }}>No failures detected</div>
        )}
        {data?.failures?.map((f, i) => (
          <div key={i} style={{ padding: "6px 0", fontSize: 13 }}>
            <span style={{ color: C.red }}>"{f.command}"</span>
            <span style={{ color: C.gray, marginLeft: 8 }}>— {f.reason}</span>
          </div>
        ))}
      </Card>
    </div>
  );
}

// -------------------------
// REFLECTIONS TAB
// -------------------------
function ReflectionsTab() {
  const { data, loading } = useApi("/reflections?limit=20");

  const verdictColor = (v) =>
    v === "success" ? C.teal : v === "partial" ? C.amber : C.red;

  if (loading) return <div style={{ color: C.gray, padding: 20 }}>Loading...</div>;

  return (
    <div>
      <Card title="Fury's self-reflections" accent={C.coral}>
        {data?.items?.map((r, i) => (
          <div key={i} style={{
            padding: "12px 0",
            borderBottom: i < data.items.length - 1
              ? "1px solid var(--color-border-tertiary)" : "none"
          }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
              <div style={{ fontSize: 13, fontWeight: 500 }}>{r.command}</div>
              <Badge text={r.verdict} color={verdictColor(r.verdict)} />
            </div>
            <div style={{ fontSize: 12, color: "var(--color-text-secondary)", marginBottom: 2 }}>
              ✓ {r.what_worked}
            </div>
            {r.what_failed && (
              <div style={{ fontSize: 12, color: C.red, marginBottom: 2 }}>
                ✗ {r.what_failed}
              </div>
            )}
            {r.improvement && (
              <div style={{ fontSize: 12, color: C.amber }}>
                → {r.improvement}
              </div>
            )}
            <div style={{ fontSize: 11, color: C.gray, marginTop: 4 }}>
              {r.timestamp?.slice(0, 19)}
            </div>
          </div>
        ))}
      </Card>
    </div>
  );
}

// -------------------------
// SKILLS TAB (Step 124)
// -------------------------
function SkillsTab() {
  const { data, loading, refetch } = useApi("/skills");
  const { data: custom, refetch: refetchCustom } = useApi("/skills/list-custom");
  const [importing, setImporting] = useState(false);
  const [msg, setMsg] = useState("");

  const handleExport = () => {
    window.open(`${API}/skills/export`, "_blank");
  };

  const handleImport = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setImporting(true);
    setMsg("");
    try {
      const form = new FormData();
      form.append("file", file);
      const res = await axios.post(`${API}/skills/import`, form);
      setMsg(`Imported: ${res.data.filename}`);
      refetchCustom();
    } catch (err) {
      setMsg(`Import failed: ${err.response?.data?.detail || err.message}`);
    } finally {
      setImporting(false);
    }
  };

  if (loading) return <div style={{ color: C.gray, padding: 20 }}>Loading...</div>;

  return (
    <div>
      <Card title="Built-in skills" accent={C.teal}>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
          {data?.skills?.map((s, i) => (
            <Badge key={i} text={s} color={C.teal} />
          ))}
        </div>
        <div style={{ fontSize: 12, color: C.gray, marginTop: 8 }}>
          {data?.count} skills registered
        </div>
      </Card>

      <Card title="Custom skills — share" accent={C.purple}>
        <div style={{ display: "flex", gap: 10, marginBottom: 12 }}>
          <button onClick={handleExport} style={{
            background: C.purple, color: "#fff", border: "none",
            borderRadius: 8, padding: "8px 16px", cursor: "pointer", fontSize: 13
          }}>
            Export skills (.zip)
          </button>
          <label style={{
            background: C.teal, color: "#fff", border: "none",
            borderRadius: 8, padding: "8px 16px", cursor: "pointer", fontSize: 13
          }}>
            Import skill (.py)
            <input
              type="file" accept=".py" onChange={handleImport}
              style={{ display: "none" }}
            />
          </label>
        </div>

        {msg && (
          <div style={{
            fontSize: 13, color: msg.includes("failed") ? C.red : C.teal,
            marginBottom: 10
          }}>
            {msg}
          </div>
        )}

        {custom?.skills?.length === 0 && (
          <div style={{ fontSize: 13, color: C.gray }}>
            No custom skills yet. Import a .py skill file to get started.
          </div>
        )}
        {custom?.skills?.map((s, i) => (
          <div key={i} style={{
            display: "flex", justifyContent: "space-between",
            padding: "6px 0", fontSize: 13,
            borderBottom: i < custom.skills.length - 1
              ? "1px solid var(--color-border-tertiary)" : "none"
          }}>
            <span>{s.filename}</span>
            <span style={{ color: C.gray, fontSize: 11 }}>
              {(s.size / 1024).toFixed(1)}kb — {s.modified?.slice(0, 10)}
            </span>
          </div>
        ))}
      </Card>
    </div>
  );
}

// -------------------------
// KNOWLEDGE TAB
// -------------------------
function KnowledgeTab() {
  const { data, loading } = useApi("/knowledge?limit=20");
  const [search, setSearch] = useState("");
  const [concept, setConcept] = useState(null);
  const [conceptData, setConceptData] = useState(null);

  const lookupConcept = async (name) => {
    setConcept(name);
    try {
      const res = await axios.get(`${API}/knowledge/${name}`);
      setConceptData(res.data);
    } catch {
      setConceptData(null);
    }
  };

  const filtered = data?.nodes?.filter(n =>
    !search || n.name.includes(search.toLowerCase())
  ) || [];

  if (loading) return <div style={{ color: C.gray, padding: 20 }}>Loading...</div>;

  return (
    <div>
      <Card title="Knowledge graph — top nodes" accent={C.blue}>
        <input
          placeholder="Search concept..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          style={{
            width: "100%", padding: "8px 12px", marginBottom: 12,
            border: "1px solid var(--color-border-secondary)",
            borderRadius: 8, fontSize: 13, boxSizing: "border-box",
            background: "var(--color-background-primary)",
            color: "var(--color-text-primary)"
          }}
        />
        <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
          {filtered.map((n, i) => (
            <button key={i} onClick={() => lookupConcept(n.name)} style={{
              background: "transparent",
              border: `1px solid ${C.blue}44`,
              borderRadius: 20, padding: "4px 12px",
              cursor: "pointer", fontSize: 12,
              color: "var(--color-text-primary)"
            }}>
              {n.name} <span style={{ color: C.gray }}>({n.count})</span>
            </button>
          ))}
        </div>
      </Card>

      {concept && conceptData && (
        <Card title={`What Fury knows about "${concept}"`} accent={C.purple}>
          {conceptData.knows?.map((k, i) => (
            <div key={i} style={{ fontSize: 13, padding: "3px 0", color: "var(--color-text-secondary)" }}>
              {concept} →[{k.relation}]→ <strong>{k.target}</strong>
              <span style={{ color: C.gray, fontSize: 11, marginLeft: 6 }}>w={k.weight}</span>
            </div>
          ))}
          {conceptData.known_by?.map((k, i) => (
            <div key={i} style={{ fontSize: 13, padding: "3px 0", color: "var(--color-text-secondary)" }}>
              <strong>{k.source}</strong> →[{k.relation}]→ {concept}
              <span style={{ color: C.gray, fontSize: 11, marginLeft: 6 }}>w={k.weight}</span>
            </div>
          ))}
          {!conceptData.knows?.length && !conceptData.known_by?.length && (
            <div style={{ color: C.gray, fontSize: 13 }}>No connections yet.</div>
          )}
        </Card>
      )}
    </div>
  );
}

// -------------------------
// COMMAND BAR
// -------------------------
function CommandBar({ onSend }) {
  const [cmd, setCmd] = useState("");
  const [sending, setSending] = useState(false);
  const [result, setResult] = useState("");

  const send = async () => {
    if (!cmd.trim()) return;
    setSending(true);
    setResult("");
    try {
      await axios.post(`${API}/command`, { command: cmd });
      setResult("Queued!");
      setCmd("");
    } catch (e) {
      setResult("Failed: " + (e.response?.data?.detail || e.message));
    } finally {
      setSending(false);
    }
  };

  return (
    <div style={{
      position: "sticky", bottom: 0,
      background: "var(--color-background-primary)",
      borderTop: "1px solid var(--color-border-tertiary)",
      padding: "12px 20px",
      display: "flex", gap: 8, alignItems: "center"
    }}>
      <input
        placeholder="Send command to Fury..."
        value={cmd}
        onChange={e => setCmd(e.target.value)}
        onKeyDown={e => e.key === "Enter" && send()}
        style={{
          flex: 1, padding: "10px 14px",
          border: "1px solid var(--color-border-secondary)",
          borderRadius: 8, fontSize: 14,
          background: "var(--color-background-secondary)",
          color: "var(--color-text-primary)"
        }}
      />
      <button onClick={send} disabled={sending} style={{
        background: C.purple, color: "#fff",
        border: "none", borderRadius: 8,
        padding: "10px 20px", cursor: "pointer",
        fontSize: 14, fontWeight: 500,
        opacity: sending ? 0.6 : 1
      }}>
        {sending ? "Sending..." : "Run"}
      </button>
      {result && (
        <span style={{
          fontSize: 13,
          color: result.includes("Failed") ? C.red : C.teal
        }}>
          {result}
        </span>
      )}
    </div>
  );
}

// -------------------------
// MAIN APP
// -------------------------
export default function App() {
  const [tab, setTab] = useState("Overview");

  const renderTab = () => {
    switch (tab) {
      case "Overview":     return <OverviewTab />;
      case "History":      return <HistoryTab />;
      case "Patterns":     return <PatternsTab />;
      case "Reflections":  return <ReflectionsTab />;
      case "Skills":       return <SkillsTab />;
      case "Knowledge":    return <KnowledgeTab />;
      default:             return <OverviewTab />;
    }
  };

  return (
    <div style={{
      minHeight: "100vh",
      background: "var(--color-background-tertiary, #f5f4ef)",
      fontFamily: "var(--font-sans, system-ui, sans-serif)",
      display: "flex", flexDirection: "column"
    }}>
      {/* Header */}
      <div style={{
        background: "var(--color-background-primary, #fff)",
        borderBottom: "1px solid var(--color-border-tertiary)",
        padding: "0 24px",
        display: "flex", alignItems: "center", gap: 24,
        height: 52
      }}>
        <div style={{ fontSize: 16, fontWeight: 500, color: C.purple }}>
          🔥 Fury Dashboard
        </div>
        <div style={{ display: "flex", gap: 4 }}>
          {TABS.map(t => (
            <button key={t} onClick={() => setTab(t)} style={{
              background: tab === t ? C.purple + "15" : "transparent",
              color: tab === t ? C.purple : "var(--color-text-secondary)",
              border: "none", borderRadius: 6,
              padding: "6px 14px", cursor: "pointer",
              fontSize: 13, fontWeight: tab === t ? 500 : 400
            }}>
              {t}
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div style={{ flex: 1, maxWidth: 860, margin: "0 auto", width: "100%", padding: "20px 24px" }}>
        {renderTab()}
      </div>

      {/* Command bar */}
      <CommandBar />
    </div>
  );
}