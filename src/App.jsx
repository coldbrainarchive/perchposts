import { Component, useCallback, useEffect, useRef, useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link, useLocation, useNavigate, useParams, useSearchParams } from "react-router-dom";

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, message: "" };
  }

  static getDerivedStateFromError(error) {
    return {
      hasError: true,
      message: error?.message || "Unknown error"
    };
  }

  componentDidCatch(error, info) {
    console.error("App render failed", error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div
          style={{
            minHeight: "100vh",
            display: "grid",
            placeItems: "center",
            padding: 24,
            background: "#16171d",
            color: "#f8fafc"
          }}
        >
          <div
            style={{
              width: "min(640px, 100%)",
              padding: 24,
              borderRadius: 18,
              border: "1px solid #2e303a",
              background: "linear-gradient(180deg, #1b1d24 0%, #14161c 100%)",
              boxShadow: "0 18px 50px rgba(0, 0, 0, 0.35)"
            }}
          >
            <h2 style={{ marginBottom: 12 }}>Something went wrong loading the forum</h2>
            <p style={{ color: "#cbd5e1" }}>{this.state.message}</p>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

// ==============================
// HELPERS
// ==============================

function getUserColor(id, username) {
  const seed = username || (id ? id.slice(0, 8) : null);
  if (!seed) return "#dbe4ee";

  let hash = 0;
  for (let i = 0; i < seed.length; i++) {
    hash = seed.charCodeAt(i) + ((hash << 5) - hash);
  }

  let hue = Math.abs(hash) % 360;

  // Keep the moderator purple exclusive to mods.
  if (hue >= 250 && hue <= 320) {
    hue = (hue + 90) % 360;
  }

  return `hsl(${hue}, 72%, 68%)`;
}

function timeAgo(date) {
  if (!date) return "";
  const str = String(date).replace(" ", "T").replace(/([+-]\d{2}:\d{2}|Z)?$/, (m) => m || "Z");
  const seconds = Math.floor((new Date() - new Date(str)) / 1000);
  if (seconds < 60) return `${seconds}s ago`;
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  return `${Math.floor(seconds / 86400)}d ago`;
}

function shortId(id) {
  return id?.slice(0, 6) || "??????";
}

function getBrowserId() {
  let id = localStorage.getItem("browser_id");
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem("browser_id", id);
  }
  return id;
}

function getModName() {
  return localStorage.getItem("mod_name") || "Mod";
}

function isModPost(record) {
  return record?.is_mod === true;
}

function isAdminPost(record) {
  return record?.is_admin === true;
}

function isStaffPost(record) {
  return record?.is_mod === true;
}

function getRoleBadge(record) {
  if (!record) return null;
  if (record.browser_id && String(record.browser_id).startsWith("bot-")) return "🤖";
  if (record.is_admin) return "🐧";
  if (record.is_mod) return "🐦";
  if (record.username) return "🐤";
  return null;
}

// Returns true if this record belongs to staff (mod/admin/bot) — gets purple accent pill
function isStaffRecord(record) {
  if (!record) return false;
  if (record.browser_id && String(record.browser_id).startsWith("bot-")) return true;
  return record.is_admin === true || record.is_mod === true;
}

const BOT_PILL_COLORS = {
  NewsBot:     "#60a5fa", // blue
  SportsBot:   "#fbbf24", // yellow
  ScienceBot:  "#34d399", // green
  NatureBot:   "#86efac", // light green
};

function UserPill({ record, name, color }) {
  const badge = getRoleBadge(record);
  const isBot = record?.browser_id && String(record.browser_id).startsWith("bot-");
  const isAdmin = !isBot && record?.is_admin === true;
  const isStaff = !isBot && !isAdmin && record?.is_mod === true;
  const pillColor = isBot
    ? (BOT_PILL_COLORS[name] || "#94a3b8")
    : isAdmin ? "#f97316"
    : isStaff ? "#c084fc"
    : (color || "#8fa0b6");
  return (
    <span
      className="user-pill"
      style={{
        color: pillColor,
        background: `${pillColor}18`,
        borderColor: `${pillColor}55`,
      }}
    >
      {badge && <span className="user-pill-badge">{badge}</span>}
      <span className="user-pill-name">{name}</span>
    </span>
  );
}

function buildModMetadata(user, memberUsername) {
  const isMod = !!user && (user.role === "mod" || user.role === "admin");
  if (!isMod) {
    return {
      username: (user && memberUsername) ? memberUsername : null,
      is_mod: false,
      is_admin: false,
      moderator: false,
      author_role: "user",
      mod_user_id: null
    };
  }

  return {
    username: user.username || getModName(),
    is_mod: true,
    is_admin: user.role === "admin",
    moderator: true,
    author_role: user.role === "admin" ? "admin" : "mod",
    mod_user_id: user.id
  };
}

// ==============================
// AUTH HEADER
// ==============================
function getStoredUser() {
  try { return JSON.parse(localStorage.getItem("auth_user") || "null"); }
  catch { return null; }
}

function getAuthHeader() {
  const token = localStorage.getItem("auth_token");
  if (!token) throw new Error("No active session. Please log in again.");
  return { Authorization: `Bearer ${token}` };
}

function getOptionalAuthHeader() {
  const token = localStorage.getItem("auth_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}


function RealtimeStyles() {
  return (
    <style>{`
      .accent-purple {
        color: #c084fc;
      }

      .app-topbar {
        position: sticky;
        top: 0;
        z-index: 20;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        padding: 14px 20px;
        border-bottom: 1px solid #2e303a;
        background: rgba(11, 15, 18, 0.92);
        backdrop-filter: blur(14px);
      }

      .app-brand {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        color: #c084fc;
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.03em;
        text-decoration: none;
      }

      .app-actions {
        display: flex;
        align-items: center;
        gap: 12px;
      }

      .app-chip {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        box-sizing: border-box;
        height: 20px;
        padding: 0 7px;
        border-radius: 999px;
        background: #1f2937;
        color: #f8fafc;
        text-decoration: none;
        font-size: 9px;
        font-weight: 800;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        border: 1px solid #374151;
        white-space: nowrap;
        appearance: none;
        -webkit-appearance: none;
        cursor: pointer;
        font-family: inherit;
        line-height: 1;
      }

      .app-chip.primary {
        background: #c084fc;
        border-color: #d8b4fe;
        color: #14081d;
      }

      .home-shell {
        display: block;
        width: min(1280px, 100%);
        margin: 0 auto;
        padding: 0 20px 32px;
        box-sizing: border-box;
      }

      .search-shell {
        position: sticky;
        top: 73px;
        z-index: 15;
        margin: 16px 0 16px;
        background: #16171d;
      }

      .search-shell::before {
        content: "";
        position: absolute;
        left: 0;
        right: 0;
        top: -16px;
        height: 16px;
        background: #16171d;
        pointer-events: none;
      }

      .search-bar-wrap {
        position: relative;
      }

      .search-bar {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 6px;
        padding: 6px 12px;
        border-radius: 12px;
        border: 1px solid #2e303a;
        background: #1b1d24;
        cursor: text;
        min-height: 42px;
        transition: border-color 0.15s;
      }

      .search-bar.focused { border-color: #c084fc; }

      .search-icon { font-size: 13px; flex-shrink: 0; opacity: 0.4; }

      .search-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        height: 26px;
        padding: 0 8px;
        border-radius: 999px;
        background: rgba(192,132,252,0.15);
        border: 1px solid rgba(192,132,252,0.4);
        color: #c084fc;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        white-space: nowrap;
        flex-shrink: 0;
      }

      .board-chip { background: rgba(192,132,252,0.15); border-color: rgba(192,132,252,0.4); color: #c084fc; }
      .continent-chip { background: rgba(192,132,252,0.15); border-color: rgba(192,132,252,0.4); color: #c084fc; }
      .country-chip { background: rgba(192,132,252,0.15); border-color: rgba(192,132,252,0.4); color: #c084fc; }

      .search-chip button {
        background: none; border: none; padding: 0; margin: 0 0 0 2px;
        color: inherit; cursor: pointer; font-size: 14px; line-height: 1;
        opacity: 0.6; display: flex; align-items: center;
      }
      .search-chip button:hover { opacity: 1; }

      .search-input {
        flex: 1;
        min-width: 80px;
        border: none;
        background: transparent;
        color: #f8fafc;
        font-size: 16px;
        outline: none;
        padding: 0;
      }
      .search-input::placeholder { color: #4b5563; }

      .search-clear {
        background: none; border: none; color: #64748b;
        cursor: pointer; font-size: 18px; padding: 0; line-height: 1; flex-shrink: 0;
      }
      .search-clear:hover { color: #94a3b8; }

      .search-dropdown {
        position: absolute;
        top: calc(100% + 4px);
        left: 0; right: 0;
        background: #1e2028;
        border: 1px solid #374151;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.5);
        z-index: 100;
        max-height: 380px;
        overflow-y: auto;
        scrollbar-width: thin;
        padding: 6px 0;
      }

      .search-section-label {
        padding: 8px 14px 3px;
        font-size: 10px;
        font-weight: 700;
        color: #4b5563;
        text-transform: uppercase;
        letter-spacing: 0.08em;
      }

      .search-suggestion {
        display: flex;
        align-items: center;
        gap: 10px;
        width: 100%;
        padding: 7px 14px;
        background: none;
        border: none;
        color: #e2e8f0;
        font-size: 13px;
        cursor: pointer;
        text-align: left;
      }
      .search-suggestion:hover { background: #2d2f3a; }

      .sugg-icon { font-size: 15px; flex-shrink: 0; }
      .sugg-label { font-weight: 500; }
      .sugg-label-block { display: flex; flex-direction: column; gap: 1px; min-width: 0; overflow: hidden; }
      .sugg-title { font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
      .sugg-meta { font-size: 11px; color: #64748b; }

      .search-divider { height: 1px; background: #374151; margin: 4px 0; }
      .search-loading { padding: 12px 14px; color: #64748b; font-size: 13px; }
      .search-empty { padding: 16px 14px; color: #4b5563; font-size: 13px; text-align: center; }

      .search-columns {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0;
      }

      .search-column {
        min-width: 0;
      }

      .search-column:first-child {
        border-right: 1px solid #374151;
      }

      .home-feed {
        min-width: 0;
      }

      .feed-hero {
        margin-bottom: 18px;
        padding: 18px 20px;
        border: 1px solid #2e303a;
        border-radius: 18px;
        background: linear-gradient(180deg, #161a20 0%, #101318 100%);
        box-shadow: 0 18px 50px rgba(0, 0, 0, 0.24);
      }

      .feed-hero-copy {
        min-width: 0;
      }

      .feed-hero-title {
        color: #f8fafc;
        font-family: var(--heading);
        font-size: 38px;
        font-weight: 800;
        letter-spacing: -0.04em;
        line-height: 0.96;
      }

      .content-card {
        padding: 20px;
        border: 1px solid #2e303a;
        border-radius: 18px;
        background: linear-gradient(180deg, #1b1d24 0%, #14161c 100%);
        box-shadow: 0 18px 50px rgba(0, 0, 0, 0.2);
      }

      .feed-post-card {
        padding: 18px 20px 17px;
      }

      .feed-post-title {
        margin: 0 0 10px;
        color: #f8fafc;
        font-size: 22px;
        line-height: 1.22;
        letter-spacing: -0.01em;
        text-decoration: none;
        text-align: left;
      }

      .feed-post-header {
        margin-bottom: 0;
        color: #94a3b8;
        font-size: 14px;
        text-align: left;
      }

      .feed-post-board-row {
        display: flex;
        align-items: center;
        gap: 12px;
        min-height: 24px;
        margin-bottom: 0;
      }

      .feed-post-board-group {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        min-width: 0;
        flex-wrap: wrap;
      }

      .feed-post-time {
        margin-left: auto;
        color: #8fa0b6;
        font-size: 13px;
        font-weight: 600;
        line-height: 1.1;
        white-space: nowrap;
      }

      .feed-post-author-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 10px;
      }

      .feed-post-author {
        min-width: 0;
        font-weight: 700;
        font-size: 14px;
        line-height: 1.2;
      }

      .user-pill {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 2px 9px 2px 6px;
        border-radius: 999px;
        border: 1px solid;
        font-size: 13px;
        font-weight: 700;
        line-height: 1.4;
        white-space: nowrap;
        vertical-align: middle;
        flex-shrink: 0;
      }

      .user-pill-badge {
        font-size: 12px;
        line-height: 1;
      }

      .user-pill-name {
        max-width: 160px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .feed-post-statuses {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        flex-shrink: 0;
      }

      .feed-post-status {
        font-weight: 700;
        white-space: nowrap;
      }

      .feed-post-link {
        display: block;
        text-align: left;
        width: 100%;
        max-width: 100%;
      }

      .feed-post-main {
        margin-top: 10px;
        padding: 12px 0 14px;
        border-top: 1px solid rgba(148, 163, 184, 0.12);
        border-bottom: 1px solid rgba(148, 163, 184, 0.12);
      }

      .feed-post-content {
        margin: 0;
        color: #d4dde7;
        font-size: 15px;
        line-height: 1.52;
        text-align: left;
        overflow-wrap: anywhere;
      }

      .feed-post-seemore {
        display: inline-block;
        margin-top: 6px;
        background: none;
        border: none;
        padding: 0;
        color: #c084fc;
        font-size: 13px;
        font-weight: 700;
        cursor: pointer;
      }

      .feed-post-actions {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 6px;
        margin-top: 13px;
        width: 100%;
      }

      .feed-post-vote-group,
      .feed-post-action-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        min-height: 30px;
        padding: 0 8px;
        border-radius: 999px;
        border: 1px solid #323b48;
        background: #1d242d;
        color: #e5edf6;
        text-decoration: none;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.02em;
      }

      .feed-post-vote-group {
        padding: 0 5px;
      }

      .feed-post-action-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 20px;
        height: 20px;
        border: 0;
        border-radius: 999px;
        background: transparent;
        color: #e2e8f0;
        font-size: 12px;
        cursor: pointer;
      }

      .feed-post-action-button.active {
        background: rgba(148, 163, 184, 0.16);
        color: #f8fafc;
      }

      .feed-post-action-button.active.downvote {
        color: #f87171;
      }

      .feed-post-vote-score {
        min-width: 16px;
        line-height: 1;
        text-align: center;
      }

      .feed-post-action-pill {
        cursor: pointer;
      }

      .comments-shell {
        margin-top: 18px;
      }

      .comments-panel {
        padding: 18px 20px;
      }

      .comments-panel-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 14px;
      }

      .comments-panel-title {
        color: #f8fafc;
        font-size: 18px;
        font-weight: 800;
        letter-spacing: -0.01em;
      }

      .comments-panel-controls {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        color: #8fa0b6;
        font-size: 12px;
        font-weight: 700;
      }

      .comments-sort {
        min-height: 32px;
        padding: 0 12px;
        border-radius: 999px;
        border: 1px solid #374151;
        background: #20262f;
        color: #dbe4ee;
        font-size: 12px;
        font-weight: 700;
      }

      .comments-list {
        display: flex;
        flex-direction: column;
        gap: 14px;
      }

      .chat-panel-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 16px 10px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
      }

      .chat-window {
        flex: 1;
        min-height: 0;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 6px;
        position: relative;
        padding: 14px 12px;
        scroll-behavior: smooth;
      }

      .chat-msg {
        display: flex;
        align-items: flex-start;
        gap: 8px;
        max-width: 100%;
      }

      .chat-avatar {
        width: 28px;
        height: 28px;
        border-radius: 999px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: 800;
        color: #0f1117;
        flex-shrink: 0;
      }

      .chat-msg-body {
        display: flex;
        flex-direction: column;
        gap: 3px;
        max-width: 80%;
      }

      .chat-msg-meta {
        display: flex;
        align-items: center;
        gap: 5px;
        font-size: 11px;
        font-weight: 700;
        padding: 0 4px;
      }

      .chat-msg-time {
        font-size: 11px;
        color: #8fa0b6;
        font-weight: 400;
      }

      .chat-bubble {
        background: #1e2530;
        color: #dbe4ee;
        border-radius: 4px 18px 18px 18px;
        padding: 9px 13px;
        font-size: 14px;
        line-height: 1.45;
        cursor: pointer;
        word-break: break-word;
        transition: opacity 0.15s;
      }

      .chat-bubble:hover {
        opacity: 0.85;
      }

      .chat-bubble.highlight {
        background: rgba(192, 132, 252, 0.18);
        outline: 1.5px solid rgba(192, 132, 252, 0.5);
        transition: background 0.3s ease, outline 0.3s ease;
      }

      .chat-bubble.pending {
        opacity: 0.55;
      }

      .chat-quote-bar {
        border-left: 3px solid rgba(192,132,252,0.5);
        padding: 4px 8px;
        margin-bottom: 6px;
        border-radius: 0 6px 6px 0;
        background: rgba(148,163,184,0.07);
      }

      .chat-quote-name {
        display: block;
        font-size: 11px;
        font-weight: 700;
        color: #c084fc;
        margin-bottom: 2px;
      }

      .chat-quote-text {
        margin: 0;
        font-size: 12px;
        color: #8fa0b6;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
      }

      .chat-bubble-text {
        display: block;
        white-space: pre-wrap;
      }

      .chat-msg-footer {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 0 4px;
      }

      .chat-delete-btn {
        background: none;
        border: none;
        color: #8fa0b6;
        font-size: 11px;
        cursor: pointer;
        padding: 0;
        opacity: 0.6;
      }

      .chat-delete-btn:hover {
        opacity: 1;
      }

      .chat-compose {
        border-top: 1px solid rgba(148, 163, 184, 0.1);
        padding: 10px 12px 10px;
        display: flex;
        flex-direction: column;
        gap: 6px;
        background: #1b1d24;
        position: sticky;
        bottom: 0;
        z-index: 10;
      }

      .chat-reply-preview {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 6px 10px;
        background: rgba(148, 163, 184, 0.07);
        border-radius: 10px;
        border-left: 3px solid #c084fc;
      }

      .chat-reply-preview-inner {
        flex: 1;
        min-width: 0;
      }

      .chat-reply-preview-name {
        display: block;
        font-size: 11px;
        font-weight: 700;
        color: #c084fc;
        margin-bottom: 2px;
      }

      .chat-reply-preview-text {
        margin: 0;
        font-size: 12px;
        color: #8fa0b6;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
      }

      .chat-reply-dismiss {
        background: none;
        border: none;
        color: #8fa0b6;
        font-size: 14px;
        cursor: pointer;
        flex-shrink: 0;
        padding: 0 2px;
      }

      .chat-input-row {
        display: flex;
        align-items: flex-end;
        gap: 8px;
      }

      .chat-input-bubble {
        flex: 1;
        background: #0f1117;
        border: 1px solid #2e303a;
        border-radius: 20px;
        display: flex;
        flex-direction: column;
        transition: border-color 0.15s;
      }

      .chat-input-bubble:focus-within {
        border-color: #4b5563;
      }

      .chat-input {
        background: transparent;
        border: none;
        border-radius: 20px;
        color: #f8fafc;
        font-size: 16px;
        font-family: inherit;
        padding: 9px 14px;
        resize: none;
        max-height: 120px;
        overflow-y: auto;
        line-height: 1.4;
      }

      .chat-input::placeholder {
        color: #8fa0b6;
      }

      .chat-input:focus {
        outline: none;
      }

      .chat-send-btn {
        width: 36px;
        height: 36px;
        border-radius: 999px;
        border: none;
        background: #7c3aed;
        color: #fff;
        font-size: 16px;
        font-weight: 700;
        cursor: pointer;
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: background 0.15s;
      }

      .chat-send-btn:disabled {
        background: #2e303a;
        color: #8fa0b6;
        cursor: default;
      }

      .comment-flat {
        display: flex;
        align-items: flex-start;
        gap: 10px;
      }

.comment-avatar {
        width: 30px;
        height: 30px;
        border-radius: 999px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 800;
        color: #0f1117;
        flex-shrink: 0;
        user-select: none;
      }

      .comment-card {
        flex: 1 1 auto;
        min-width: 0;
        padding-top: 1px;
      }

      .comment-card-header {
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 8px;
        flex-wrap: nowrap;
        overflow: hidden;
      }

      .comment-header-actions {
        margin-left: auto;
        display: flex;
        align-items: center;
        gap: 6px;
        flex-shrink: 0;
      }

      .comment-footer-actions {
        display: flex;
        align-items: center;
        gap: 6px;
        margin-top: 8px;
      }

      .comment-header-btn {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        height: 24px;
        padding: 0 9px;
        border-radius: 999px;
        border: 1px solid rgba(148, 163, 184, 0.2);
        background: transparent;
        color: #c084fc;
        font-size: 11px;
        font-weight: 700;
        cursor: pointer;
        white-space: nowrap;
        transition: background 0.15s;
      }

      .comment-header-btn:hover {
        background: rgba(96, 165, 250, 0.08);
      }

      .comment-card-author {
        font-size: 13px;
        font-weight: 800;
        min-width: 0;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .comment-card-time {
        font-size: 12px;
        color: #8fa0b6;
        white-space: nowrap;
        flex-shrink: 0;
      }

      .comment-card-op {
        font-size: 11px;
        font-weight: 700;
        color: #c084fc;
      }

      .chat-action-sheet {
        display: flex;
        gap: 6px;
        margin-bottom: 5px;
      }

      .chat-action-btn {
        height: 26px;
        padding: 0 10px;
        border-radius: 999px;
        border: 1px solid rgba(148,163,184,0.2);
        background: transparent;
        color: #94a3b8;
        font-size: 12px;
        font-weight: 700;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 4px;
      }

      .chat-action-btn:hover {
        background: rgba(148,163,184,0.08);
      }

      .chat-reactions {
        display: flex;
        flex-wrap: wrap;
        gap: 4px;
        margin-top: 5px;
      }

      .chat-reaction-pill {
        display: inline-flex;
        align-items: center;
        gap: 3px;
        height: 24px;
        padding: 0 8px;
        border-radius: 999px;
        border: 1px solid rgba(148,163,184,0.2);
        background: rgba(148,163,184,0.07);
        font-size: 13px;
        cursor: pointer;
        color: #dbe4ee;
        transition: background 0.12s;
      }

      .chat-reaction-pill.mine {
        border-color: #7c3aed;
        background: rgba(124,58,237,0.15);
      }

      .chat-reaction-pill:hover {
        background: rgba(148,163,184,0.14);
      }

      .chat-reaction-count {
        font-size: 11px;
        font-weight: 700;
        color: #94a3b8;
      }

      .chat-emoji-picker-row {
        margin-top: 5px;
      }

      .chat-emoji-picker-input {
        height: 30px;
        padding: 0 12px;
        border-radius: 999px;
        border: 1px solid rgba(148,163,184,0.25);
        background: #0f1117;
        color: #f8fafc;
        font-size: 16px;
        outline: none;
        width: 140px;
      }

      .chat-emoji-picker-input::placeholder {
        color: #8fa0b6;
        font-size: 12px;
      }

      .comment-quote {
        border-left: 3px solid rgba(148, 163, 184, 0.35);
        border-radius: 0 8px 8px 0;
        background: rgba(148, 163, 184, 0.07);
        padding: 8px 12px;
        margin-bottom: 10px;
        overflow: hidden;
      }

      .comment-quote-author {
        display: block;
        font-size: 12px;
        font-weight: 700;
        color: #94a3b8;
        margin-bottom: 3px;
      }

      .comment-quote-body {
        margin: 0;
        font-size: 13px;
        line-height: 1.45;
        color: #8fa0b6;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
      }

      .comment-card-actions {
        display: inline-flex;
        align-items: center;
        gap: 2px;
        margin-top: 10px;
      }

      .comment-action {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        height: 28px;
        padding: 0 8px;
        border: none;
        border-radius: 999px;
        background: transparent;
        color: #8fa0b6;
        font-size: 12px;
        font-weight: 700;
        cursor: pointer;
        transition: background 0.15s, color 0.15s;
      }

      .comment-action:hover {
        background: rgba(148, 163, 184, 0.1);
        color: #f8fafc;
      }

      .comment-body {
        color: #d4dde7;
        font-size: 15px;
        line-height: 1.5;
        white-space: pre-wrap;
        overflow-wrap: anywhere;
      }

.comment-replies-list {
        margin-top: 12px;
        padding-left: 12px;
        border-left: 2px solid rgba(148, 163, 184, 0.15);
        display: flex;
        flex-direction: column;
        gap: 14px;
      }

      .comment-composer {
        margin-bottom: 20px;
        padding-bottom: 20px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.12);
      }

      .comment-composer-textarea {
        width: 100%;
        box-sizing: border-box;
        background: #0f1117;
        border: 1px solid #2e303a;
        border-radius: 10px;
        color: #f8fafc;
        font-size: 16px;
        font-family: inherit;
        padding: 10px 12px;
        resize: none;
        min-height: 60px;
      }

      .comment-composer-textarea::placeholder {
        color: #8fa0b6;
      }

      .comment-composer-textarea:focus {
        outline: none;
        border-color: #4b5563;
      }

      .comment-composer-actions {
        display: flex;
        justify-content: flex-end;
        gap: 6px;
        margin-top: 8px;
      }

      .comment-composer-cancel {
        height: 28px;
        padding: 0 12px;
        border-radius: 999px;
        border: none;
        background: #2e303a;
        color: #dbe4ee;
        font-size: 12px;
        font-weight: 700;
        cursor: pointer;
      }

      .comment-composer-submit {
        height: 28px;
        padding: 0 14px;
        border-radius: 999px;
        border: none;
        background: #c084fc;
        color: #14081d;
        font-size: 12px;
        font-weight: 700;
        cursor: pointer;
      }

      .inline-reply-box {
        margin-top: 12px;
        padding: 12px;
        border-radius: 14px;
        background: #0f1117;
        border: 1px solid #2e303a;
      }


@media (max-width: 900px) {
        .app-topbar {
          padding: 12px 14px;
        }

        .app-brand {
          font-size: 22px;
        }

        .app-actions {
          gap: 8px;
        }

        .app-chip {
          height: 20px;
          padding: 0 7px;
          font-size: 9px;
        }

        .home-shell {
          padding: 0 14px 24px;
        }

        .search-shell {
          top: 62px;
          margin: 12px 0 12px;
        }

        .search-shell::before {
          top: -12px;
          height: 12px;
        }

        .feed-hero {
          margin-bottom: 14px;
        }

        .feed-hero-title {
          font-size: 34px;
        }

        .feed-post-board-row {
          flex-wrap: nowrap;
          align-items: center;
        }

        .feed-post-author-row {
          flex-wrap: wrap;
        }

        .feed-post-board-group {
          min-width: 0;
        }

        .feed-post-statuses {
          gap: 6px;
        }

        .feed-post-time {
          margin-left: auto;
          align-self: center;
          font-size: 11px;
          line-height: 1.1;
        }

        .feed-post-card {
          padding: 14px 14px 13px;
        }

        .feed-post-header {
          margin-bottom: 0;
        }

        .feed-post-board-row {
          min-height: 22px;
          gap: 10px;
        }

        .feed-post-author {
          font-size: 13px;
        }

        .feed-post-main {
          margin-top: 8px;
          padding: 10px 0 12px;
        }

        .feed-post-title {
          font-size: 18px;
          margin-bottom: 8px;
          line-height: 1.24;
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
          overflow: hidden;
        }

        .feed-post-content {
          font-size: 14px;
          line-height: 1.5;
        }

        .feed-post-actions {
          gap: 5px;
          margin-top: 11px;
        }

        .feed-post-vote-group,
        .feed-post-action-pill {
          min-height: 28px;
          padding: 0 7px;
          font-size: 10px;
        }

        .feed-post-action-button {
          width: 18px;
          height: 18px;
          font-size: 11px;
        }

        .comments-panel {
          padding: 14px;
        }

        .comments-panel-header {
          margin-bottom: 12px;
        }

        .comment-card-header {
          align-items: center;
        }

        .comment-card-actions {
          width: 100%;
          margin-top: 8px;
          gap: 8px;
        }

        .comment-children {
          margin-top: 10px;
          padding-left: 12px;
        }
      }
    `}</style>
  );
}

const BOARDS = [
  { name: "Activity", slug: "activity", icon: "⚡", virtual: true },
  { name: "General", slug: "general", icon: "📰" },
  { name: "Sports", slug: "sports", icon: "🏈" },
  { name: "Science", slug: "science-nature", icon: "🔬" },
  { name: "Random", slug: "random", icon: "🎲" },
  { name: "Announcements", slug: "announcements", icon: "📢" },
  { name: "Feedback", slug: "feedback", icon: "💬" },
  { name: "Cage", slug: "cage", icon: "🪹" }
];

const CONTINENTS = ["World", "Asia", "Middle East", "Africa", "North America", "South America", "Europe", "Australia/Oceania"];

function getCountryFlag(name) {
  if (!name) return "";
  const entry = COUNTRIES_WITH_FLAGS.find(c => c.name === name);
  return entry ? entry.flag : "";
}


const COUNTRY_CONTINENT = {
  Albania: "Europe", Andorra: "Europe", Austria: "Europe", Belarus: "Europe",
  Belgium: "Europe", "Bosnia & Herzegovina": "Europe", Bulgaria: "Europe",
  Croatia: "Europe", Cyprus: "Europe", "Czech Republic": "Europe",
  Denmark: "Europe", Estonia: "Europe", Finland: "Europe", France: "Europe",
  Georgia: "Europe", Germany: "Europe", Greece: "Europe", Hungary: "Europe",
  Iceland: "Europe", Ireland: "Europe", Italy: "Europe", Kosovo: "Europe",
  Latvia: "Europe", Liechtenstein: "Europe", Lithuania: "Europe",
  Luxembourg: "Europe", Malta: "Europe", Moldova: "Europe", Monaco: "Europe",
  Montenegro: "Europe", Netherlands: "Europe", "North Macedonia": "Europe",
  Norway: "Europe", Poland: "Europe", Portugal: "Europe", Romania: "Europe",
  Russia: "Europe", Serbia: "Europe", Slovakia: "Europe", Slovenia: "Europe",
  Spain: "Europe", Sweden: "Europe", Switzerland: "Europe", Ukraine: "Europe",
  "United Kingdom": "Europe",
  Afghanistan: "Asia", Armenia: "Asia", Azerbaijan: "Asia", Bangladesh: "Asia",
  Bhutan: "Asia", Brunei: "Asia", Cambodia: "Asia", China: "Asia",
  India: "Asia", Indonesia: "Asia", Japan: "Asia", Kazakhstan: "Asia",
  Kyrgyzstan: "Asia", Laos: "Asia", Malaysia: "Asia", Maldives: "Asia",
  Mongolia: "Asia", Myanmar: "Asia", Nepal: "Asia", "North Korea": "Asia",
  Pakistan: "Asia", Philippines: "Asia", Singapore: "Asia", "South Korea": "Asia",
  "Sri Lanka": "Asia", Taiwan: "Asia", Tajikistan: "Asia", Thailand: "Asia",
  Turkmenistan: "Asia", Uzbekistan: "Asia", Vietnam: "Asia",
  Bahrain: "Middle East", Iran: "Middle East", Iraq: "Middle East",
  Israel: "Middle East", Jordan: "Middle East", Kuwait: "Middle East",
  Lebanon: "Middle East", Oman: "Middle East", Palestine: "Middle East",
  Qatar: "Middle East", "Saudi Arabia": "Middle East", Syria: "Middle East",
  Turkey: "Middle East", "United Arab Emirates": "Middle East", Yemen: "Middle East",
  Algeria: "Africa", Angola: "Africa", Benin: "Africa", Botswana: "Africa",
  "Burkina Faso": "Africa", Burundi: "Africa", Cameroon: "Africa", Chad: "Africa",
  Congo: "Africa", "DR Congo": "Africa", Egypt: "Africa", Eritrea: "Africa",
  Eswatini: "Africa", Ethiopia: "Africa", Gabon: "Africa", Gambia: "Africa",
  Ghana: "Africa", Guinea: "Africa", Kenya: "Africa", Liberia: "Africa",
  Libya: "Africa", Madagascar: "Africa", Malawi: "Africa", Mali: "Africa",
  Mauritania: "Africa", Mauritius: "Africa", Morocco: "Africa",
  Mozambique: "Africa", Namibia: "Africa", Niger: "Africa", Nigeria: "Africa",
  Rwanda: "Africa", Senegal: "Africa", "Sierra Leone": "Africa", Somalia: "Africa",
  "South Africa": "Africa", "South Sudan": "Africa", Sudan: "Africa",
  Tanzania: "Africa", Togo: "Africa", Tunisia: "Africa", Uganda: "Africa",
  Zambia: "Africa", Zimbabwe: "Africa",
  Bahamas: "North America", Belize: "North America", Canada: "North America",
  "Costa Rica": "North America", Cuba: "North America",
  "Dominican Republic": "North America", "El Salvador": "North America",
  Guatemala: "North America", Haiti: "North America", Honduras: "North America",
  Jamaica: "North America", Mexico: "North America", Nicaragua: "North America",
  Panama: "North America", "Trinidad & Tobago": "North America",
  "United States": "North America",
  Argentina: "South America", Bolivia: "South America", Brazil: "South America",
  Chile: "South America", Colombia: "South America", Ecuador: "South America",
  Paraguay: "South America", Peru: "South America", Uruguay: "South America",
  Venezuela: "South America",
  Australia: "Australia/Oceania", Fiji: "Australia/Oceania",
  "New Zealand": "Australia/Oceania", "Papua New Guinea": "Australia/Oceania",
};

const COUNTRIES_WITH_FLAGS = [
  { name: "Afghanistan", flag: "🇦🇫" }, { name: "Albania", flag: "🇦🇱" }, { name: "Algeria", flag: "🇩🇿" },
  { name: "Andorra", flag: "🇦🇩" }, { name: "Angola", flag: "🇦🇴" }, { name: "Argentina", flag: "🇦🇷" },
  { name: "Armenia", flag: "🇦🇲" }, { name: "Australia", flag: "🇦🇺" }, { name: "Austria", flag: "🇦🇹" },
  { name: "Azerbaijan", flag: "🇦🇿" }, { name: "Bahamas", flag: "🇧🇸" }, { name: "Bahrain", flag: "🇧🇭" },
  { name: "Bangladesh", flag: "🇧🇩" }, { name: "Belarus", flag: "🇧🇾" }, { name: "Belgium", flag: "🇧🇪" },
  { name: "Belize", flag: "🇧🇿" }, { name: "Benin", flag: "🇧🇯" }, { name: "Bhutan", flag: "🇧🇹" },
  { name: "Bolivia", flag: "🇧🇴" }, { name: "Bosnia & Herzegovina", flag: "🇧🇦" }, { name: "Botswana", flag: "🇧🇼" },
  { name: "Brazil", flag: "🇧🇷" }, { name: "Brunei", flag: "🇧🇳" }, { name: "Bulgaria", flag: "🇧🇬" },
  { name: "Burkina Faso", flag: "🇧🇫" }, { name: "Burundi", flag: "🇧🇮" }, { name: "Cambodia", flag: "🇰🇭" },
  { name: "Cameroon", flag: "🇨🇲" }, { name: "Canada", flag: "🇨🇦" }, { name: "Chad", flag: "🇹🇩" },
  { name: "Chile", flag: "🇨🇱" }, { name: "China", flag: "🇨🇳" }, { name: "Colombia", flag: "🇨🇴" },
  { name: "Congo", flag: "🇨🇬" }, { name: "Costa Rica", flag: "🇨🇷" }, { name: "Croatia", flag: "🇭🇷" },
  { name: "Cuba", flag: "🇨🇺" }, { name: "Cyprus", flag: "🇨🇾" }, { name: "Czech Republic", flag: "🇨🇿" },
  { name: "Denmark", flag: "🇩🇰" }, { name: "Dominican Republic", flag: "🇩🇴" }, { name: "DR Congo", flag: "🇨🇩" },
  { name: "Ecuador", flag: "🇪🇨" }, { name: "Egypt", flag: "🇪🇬" }, { name: "El Salvador", flag: "🇸🇻" },
  { name: "Eritrea", flag: "🇪🇷" }, { name: "Estonia", flag: "🇪🇪" }, { name: "Eswatini", flag: "🇸🇿" },
  { name: "Ethiopia", flag: "🇪🇹" }, { name: "Fiji", flag: "🇫🇯" }, { name: "Finland", flag: "🇫🇮" },
  { name: "France", flag: "🇫🇷" }, { name: "Gabon", flag: "🇬🇦" }, { name: "Gambia", flag: "🇬🇲" },
  { name: "Georgia", flag: "🇬🇪" }, { name: "Germany", flag: "🇩🇪" }, { name: "Ghana", flag: "🇬🇭" },
  { name: "Greece", flag: "🇬🇷" }, { name: "Guatemala", flag: "🇬🇹" }, { name: "Guinea", flag: "🇬🇳" },
  { name: "Haiti", flag: "🇭🇹" }, { name: "Honduras", flag: "🇭🇳" }, { name: "Hungary", flag: "🇭🇺" },
  { name: "Iceland", flag: "🇮🇸" }, { name: "India", flag: "🇮🇳" }, { name: "Indonesia", flag: "🇮🇩" },
  { name: "Iran", flag: "🇮🇷" }, { name: "Iraq", flag: "🇮🇶" }, { name: "Ireland", flag: "🇮🇪" },
  { name: "Israel", flag: "🇮🇱" }, { name: "Italy", flag: "🇮🇹" }, { name: "Jamaica", flag: "🇯🇲" },
  { name: "Japan", flag: "🇯🇵" }, { name: "Jordan", flag: "🇯🇴" }, { name: "Kazakhstan", flag: "🇰🇿" },
  { name: "Kenya", flag: "🇰🇪" }, { name: "Kosovo", flag: "🇽🇰" }, { name: "Kuwait", flag: "🇰🇼" },
  { name: "Kyrgyzstan", flag: "🇰🇬" }, { name: "Laos", flag: "🇱🇦" }, { name: "Latvia", flag: "🇱🇻" },
  { name: "Lebanon", flag: "🇱🇧" }, { name: "Liberia", flag: "🇱🇷" }, { name: "Libya", flag: "🇱🇾" },
  { name: "Liechtenstein", flag: "🇱🇮" }, { name: "Lithuania", flag: "🇱🇹" }, { name: "Luxembourg", flag: "🇱🇺" },
  { name: "Madagascar", flag: "🇲🇬" }, { name: "Malawi", flag: "🇲🇼" }, { name: "Malaysia", flag: "🇲🇾" },
  { name: "Maldives", flag: "🇲🇻" }, { name: "Mali", flag: "🇲🇱" }, { name: "Malta", flag: "🇲🇹" },
  { name: "Mauritania", flag: "🇲🇷" }, { name: "Mauritius", flag: "🇲🇺" }, { name: "Mexico", flag: "🇲🇽" },
  { name: "Moldova", flag: "🇲🇩" }, { name: "Monaco", flag: "🇲🇨" }, { name: "Mongolia", flag: "🇲🇳" },
  { name: "Montenegro", flag: "🇲🇪" }, { name: "Morocco", flag: "🇲🇦" }, { name: "Mozambique", flag: "🇲🇿" },
  { name: "Myanmar", flag: "🇲🇲" }, { name: "Namibia", flag: "🇳🇦" }, { name: "Nepal", flag: "🇳🇵" },
  { name: "Netherlands", flag: "🇳🇱" }, { name: "New Zealand", flag: "🇳🇿" }, { name: "Nicaragua", flag: "🇳🇮" },
  { name: "Niger", flag: "🇳🇪" }, { name: "Nigeria", flag: "🇳🇬" }, { name: "North Korea", flag: "🇰🇵" },
  { name: "North Macedonia", flag: "🇲🇰" }, { name: "Norway", flag: "🇳🇴" }, { name: "Oman", flag: "🇴🇲" },
  { name: "Pakistan", flag: "🇵🇰" }, { name: "Palestine", flag: "🇵🇸" }, { name: "Panama", flag: "🇵🇦" },
  { name: "Papua New Guinea", flag: "🇵🇬" }, { name: "Paraguay", flag: "🇵🇾" }, { name: "Peru", flag: "🇵🇪" },
  { name: "Philippines", flag: "🇵🇭" }, { name: "Poland", flag: "🇵🇱" }, { name: "Portugal", flag: "🇵🇹" },
  { name: "Qatar", flag: "🇶🇦" }, { name: "Romania", flag: "🇷🇴" }, { name: "Russia", flag: "🇷🇺" },
  { name: "Rwanda", flag: "🇷🇼" }, { name: "Saudi Arabia", flag: "🇸🇦" }, { name: "Senegal", flag: "🇸🇳" },
  { name: "Serbia", flag: "🇷🇸" }, { name: "Sierra Leone", flag: "🇸🇱" }, { name: "Singapore", flag: "🇸🇬" },
  { name: "Slovakia", flag: "🇸🇰" }, { name: "Slovenia", flag: "🇸🇮" }, { name: "Somalia", flag: "🇸🇴" },
  { name: "South Africa", flag: "🇿🇦" }, { name: "South Korea", flag: "🇰🇷" }, { name: "South Sudan", flag: "🇸🇸" },
  { name: "Spain", flag: "🇪🇸" }, { name: "Sri Lanka", flag: "🇱🇰" }, { name: "Sudan", flag: "🇸🇩" },
  { name: "Sweden", flag: "🇸🇪" }, { name: "Switzerland", flag: "🇨🇭" }, { name: "Syria", flag: "🇸🇾" },
  { name: "Taiwan", flag: "🇹🇼" }, { name: "Tajikistan", flag: "🇹🇯" }, { name: "Tanzania", flag: "🇹🇿" },
  { name: "Thailand", flag: "🇹🇭" }, { name: "Togo", flag: "🇹🇬" }, { name: "Trinidad & Tobago", flag: "🇹🇹" },
  { name: "Tunisia", flag: "🇹🇳" }, { name: "Turkey", flag: "🇹🇷" }, { name: "Turkmenistan", flag: "🇹🇲" },
  { name: "Uganda", flag: "🇺🇬" }, { name: "Ukraine", flag: "🇺🇦" }, { name: "United Arab Emirates", flag: "🇦🇪" },
  { name: "United Kingdom", flag: "🇬🇧" }, { name: "United States", flag: "🇺🇸" }, { name: "Uruguay", flag: "🇺🇾" },
  { name: "Uzbekistan", flag: "🇺🇿" }, { name: "Venezuela", flag: "🇻🇪" }, { name: "Vietnam", flag: "🇻🇳" },
  { name: "Yemen", flag: "🇾🇪" }, { name: "Zambia", flag: "🇿🇲" }, { name: "Zimbabwe", flag: "🇿🇼" },
];

function getBoardBySlug(slug) {
  return BOARDS.find((board) => board.slug === slug) || null;
}

function getBoardNameFromPost(post) {
  const boardValue = post?.board || post?.category || post?.community_id || "";
  const normalizedValue = String(boardValue).trim().toLowerCase();

  if (!normalizedValue) return "";

  const aliased = normalizedValue === "politics" ? "general" : normalizedValue;
  const matchedBoard = BOARDS.find(
    (board) => board.slug === aliased || board.name.toLowerCase() === aliased
  );

  return matchedBoard?.name || String(boardValue).trim();
}

function filterPostsForBoard(posts, boardName) {
  if (!boardName) return posts;
  return posts.filter((post) => getBoardNameFromPost(post) === boardName);
}

const BOARD_TAGS_STORAGE_KEY = "board_tags_by_post_id";
const PENDING_BOARD_TAGS_STORAGE_KEY = "pending_board_tags";
const POST_REACTIONS_STORAGE_KEY = "post_reactions_by_browser";
const WORKER_URL = "https://daboysforumip.coldbrainarchive.workers.dev";
const BOT_USERNAMES = ["NewsBot", "ScienceBot", "NatureBot", "SportsBot"];

const BIRD_NAMES = [
  "albatross","avocet","bald-eagle","barn-owl","barn-swallow","bateleur",
  "bee-eater","belted-kingfisher","bittern","black-swan","blackbird","bluebird",
  "blue-jay","blue-tit","booby","bowerbird","brambling","bufflehead",
  "bullfinch","bunting","bustard","buzzard","canary","caracara","cardinal",
  "cassowary","cedar-waxwing","chaffinch","chickadee","chimney-swift","chough",
  "chukar","cockatiel","condor","coot","cormorant","crane","crossbill","crow",
  "cuckoo","curlew","darter","dipper","diving-petrel","dotterel","dunlin",
  "dunno","eagle-owl","egret","eider","emu","falcon","fieldfare","flamingo",
  "flicker","flycatcher","frigatebird","fulmar","gadwall","galah","gannet",
  "garganey","godwit","goldcrest","golden-eagle","goldeneye","goldfinch",
  "goosander","goshawk","grackle","grebe","grosbeak","grouse","guillemot",
  "gull","hamerkop","harrier","hawfinch","heron","hobby","honeyeater",
  "hoopoe","hornbill","hummingbird","ibis","jackdaw","jacamar","jaeger",
  "jay","junco","kestrel","killdeer","kingfisher","kite","kittiwake",
  "knot","kookaburra","lark","laughingthrush","linnet","loon","lorikeet",
  "lyrebird","magpie","mallard","manakin","martin","meadowlark","merganser",
  "merlin","mockingbird","motmot","murre","myna","nighthawk","nightingale",
  "nightjar","noddy","nuthatch","oriole","osprey","ovenbird","oystercatcher",
  "peregrine","petrel","phoebe","pigeon","pintail","pipit","plover",
  "pochard","potoo","puffin","pygmy-owl","quail","raven","razorbill",
  "redstart","redwing","roadrunner","robin","rosella","ruff","sandpiper",
  "sapsucker","scaup","shoveler","shrike","siskin","skimmer","skua",
  "skylark","snipe","sparrow","spoonbill","starling","stilt","stork",
  "swallow","swan","swift","tanager","teal","tern","thrush","tit",
  "towhee","trogon","tropicbird","toucan","turnstone","veery","vireo",
  "vulture","warbler","waxwing","wheatear","whimbrel","wigeon","woodcock",
  "woodpecker","wren","yellowthroat","falcon","finch","flicker","parrot",
  "pelican","penguin","pheasant","pitta","plover","quetzal",
];

function generateBirdUsername() {
  const bird = BIRD_NAMES[Math.floor(Math.random() * BIRD_NAMES.length)];
  const num = String(Math.floor(Math.random() * 9000) + 1000);
  return `${bird}-${num}`;
}
const STANDARD_REACTIONS = [
  "😀", "😁", "😂", "🤣", "😊", "😍", "😘", "😎",
  "🤔", "😮", "😢", "😭", "😡", "👏", "🙌", "🙏",
  "👍", "👎", "❤️", "🔥", "🎉", "💯", "👀", "🤝"
];

function readStorageJson(key, fallback) {
  if (typeof window === "undefined") return fallback;

  try {
    const rawValue = window.localStorage.getItem(key);
    return rawValue ? JSON.parse(rawValue) : fallback;
  } catch {
    return fallback;
  }
}

function writeStorageJson(key, value) {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(key, JSON.stringify(value));
}

function getStoredBoardTagsByPostId() {
  return readStorageJson(BOARD_TAGS_STORAGE_KEY, {});
}

function setStoredBoardTagsByPostId(tags) {
  writeStorageJson(BOARD_TAGS_STORAGE_KEY, tags);
}

function getPendingBoardTags() {
  return readStorageJson(PENDING_BOARD_TAGS_STORAGE_KEY, []);
}

function setPendingBoardTags(tags) {
  writeStorageJson(PENDING_BOARD_TAGS_STORAGE_KEY, tags);
}

function queuePendingBoardTag({ title, content, browserId, boardName }) {
  const pendingTags = getPendingBoardTags();
  pendingTags.push({
    title,
    content,
    browser_id: browserId,
    boardName,
    createdAt: Date.now()
  });
  setPendingBoardTags(pendingTags.slice(-30));
}

function rememberBoardTagForPost(postId, boardName) {
  if (!postId || !boardName) return;
  const storedTagsByPostId = getStoredBoardTagsByPostId();
  setStoredBoardTagsByPostId({
    ...storedTagsByPostId,
    [postId]: boardName
  });
}

function syncBoardTagToPostRecord({ postId, board }) {
  if (postId) rememberBoardTagForPost(postId, board.name);
}

function hydratePostsWithBoardTags(posts) {
  const storedTagsByPostId = getStoredBoardTagsByPostId();
  const pendingTags = getPendingBoardTags();
  const nextStoredTagsByPostId = { ...storedTagsByPostId };
  const remainingPendingTags = [];
  let didChangeStoredTags = false;

  const hydratedPosts = posts.map((post) => {
    const existingBoard = getBoardNameFromPost(post);
    if (existingBoard) {
      if (post.id && storedTagsByPostId[post.id] !== existingBoard) {
        nextStoredTagsByPostId[post.id] = existingBoard;
        didChangeStoredTags = true;
      }

      return post;
    }

    const storedBoard = post.id ? storedTagsByPostId[post.id] : "";
    if (storedBoard) {
      return { ...post, board: storedBoard };
    }

    const matchedPendingTagIndex = pendingTags.findIndex((tag) => (
      tag.browser_id === post.browser_id &&
      tag.title === post.title &&
      tag.content === post.content
    ));

    if (matchedPendingTagIndex >= 0) {
      const matchedPendingTag = pendingTags[matchedPendingTagIndex];

      if (post.id) {
        nextStoredTagsByPostId[post.id] = matchedPendingTag.boardName;
        didChangeStoredTags = true;
      }

      pendingTags.splice(matchedPendingTagIndex, 1);

      return { ...post, board: matchedPendingTag.boardName };
    }

    return post;
  });

  pendingTags.forEach((tag) => {
    if (Date.now() - tag.createdAt < 1000 * 60 * 60 * 24) {
      remainingPendingTags.push(tag);
    }
  });

  if (didChangeStoredTags) {
    setStoredBoardTagsByPostId(nextStoredTagsByPostId);
  }

  if (remainingPendingTags.length !== getPendingBoardTags().length) {
    setPendingBoardTags(remainingPendingTags);
  }

  return hydratedPosts;
}

function hydratePostWithBoardTag(post) {
  if (!post) return post;
  const [hydratedPost] = hydratePostsWithBoardTags([post]);
  return hydratedPost;
}


function getStoredPostReactions() {
  return readStorageJson(POST_REACTIONS_STORAGE_KEY, {});
}

function setStoredPostReactions(reactions) {
  writeStorageJson(POST_REACTIONS_STORAGE_KEY, reactions);
}

function getReactionStateForPost(postId) {
  const reactionsByPost = getStoredPostReactions();
  const postReactions = reactionsByPost[postId] || {};
  const counts = {};

  Object.values(postReactions).forEach((emoji) => {
    counts[emoji] = (counts[emoji] || 0) + 1;
  });

  return {
    counts,
    selectedReaction: postReactions[getBrowserId()] || ""
  };
}

function toggleReactionForPost(postId, emoji) {
  const browserId = getBrowserId();
  const reactionsByPost = getStoredPostReactions();
  const postReactions = {
    ...(reactionsByPost[postId] || {})
  };

  if (postReactions[browserId] === emoji) {
    delete postReactions[browserId];
  } else {
    postReactions[browserId] = emoji;
  }

  setStoredPostReactions({
    ...reactionsByPost,
    [postId]: postReactions
  });
}

function countValidComments(commentsData) {
  const all = commentsData || [];
  const validIds = new Set();
  all.filter((c) => !c.parent_comment_id).forEach((c) => validIds.add(c.id));
  let changed = true;
  while (changed) {
    changed = false;
    all.forEach((c) => {
      if (!validIds.has(c.id) && c.parent_comment_id && validIds.has(c.parent_comment_id)) {
        validIds.add(c.id);
        changed = true;
      }
    });
  }
  const counts = {};
  all.filter((c) => validIds.has(c.id)).forEach((c) => {
    counts[c.post_id] = (counts[c.post_id] || 0) + 1;
  });
  return counts;
}

async function voteOnPost(postId, value) {
  const authHeaders = getOptionalAuthHeader();
  const res = await fetch(`${WORKER_URL}/vote-post`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders },
    body: JSON.stringify({ post_id: postId, browser_id: getBrowserId(), value, username: localStorage.getItem("mod_name") || undefined })
  });
  return res.json();
}

async function fetchReactions(commentIds) {
  if (!commentIds.length) return {};
  try {
    const res = await fetch(`${WORKER_URL}/get-reactions?comment_ids=${commentIds.join(",")}`);
    if (!res.ok) return {};
    const { reactions } = await res.json();
    const result = {};
    (reactions || []).forEach(({ comment_id, browser_id, emoji }) => {
      if (!result[comment_id]) result[comment_id] = {};
      if (!result[comment_id][emoji]) result[comment_id][emoji] = [];
      result[comment_id][emoji].push(browser_id);
    });
    return result;
  } catch { return {}; }
}

async function fetchVotesForPosts(postIds) {
  if (!postIds.length) return {};
  const browserId = getBrowserId();
  try {
    const res = await fetch(`${WORKER_URL}/get-votes?post_ids=${postIds.slice(0, 100).join(",")}`);
    if (!res.ok) return {};
    const { votes } = await res.json();
    const result = {};
    for (const postId of postIds) {
      const rows = (votes || []).filter((r) => r.post_id === postId);
      result[postId] = {
        score: rows.reduce((s, r) => s + (r.value || 0), 0),
        myVote: rows.find((r) => r.browser_id === browserId)?.value || 0,
        voteCount: rows.length
      };
    }
    return result;
  } catch { return {}; }
}

const CONTINENT_GLOBE = {
  "World":             "🌐",
  "Asia":              "🌏",
  "Middle East":       "🌍",
  "Africa":            "🌍",
  "North America":     "🌎",
  "South America":     "🌎",
  "Europe":            "🌍",
  "Australia/Oceania": "🌏",
};

function GeoBadge({ country, continent, small }) {
  if (!country && !continent) return null;
  const icon = country ? getCountryFlag(country) : (CONTINENT_GLOBE[continent] || "🌐");
  const label = country || continent;
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: small ? 4 : 6,
        height: small ? 20 : 26,
        padding: small ? "0 6px" : "0 8px",
        borderRadius: 999,
        background: "#20262f",
        color: "#dbe4ee",
        fontSize: small ? 9 : 11,
        fontWeight: 800,
        letterSpacing: "0.03em",
        textTransform: "uppercase",
        whiteSpace: "nowrap",
      }}
    >
      <span>{icon}</span>
      <span>{label}</span>
    </span>
  );
}

function BoardBadge({ boardName, small }) {
  const matchedBoard = BOARDS.find((board) => board.name === boardName);

  if (!matchedBoard) return null;

  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: small ? 4 : 6,
        height: small ? 20 : 26,
        padding: small ? "0 6px" : "0 8px",
        borderRadius: 999,
        background: "#20262f",
        color: "#dbe4ee",
        fontSize: small ? 9 : 11,
        fontWeight: 800,
        letterSpacing: "0.03em",
        textTransform: "uppercase",
        whiteSpace: "nowrap"
      }}
    >
      <span>{matchedBoard.icon}</span>
      <span>{matchedBoard.name}</span>
    </span>
  );
}

const POST_PREVIEW_LIMIT = 280;
const ATTACH_MARKER = "\n\n[ATTACH:";

function parsePostContent(raw) {
  if (!raw) return { text: raw || "", attachment: null };
  const idx = raw.indexOf(ATTACH_MARKER);
  if (idx === -1) return { text: raw, attachment: null };
  const text = raw.slice(0, idx);
  try {
    const json = raw.slice(idx + ATTACH_MARKER.length, raw.lastIndexOf("]"));
    return { text, attachment: JSON.parse(json) };
  } catch {
    return { text: raw, attachment: null };
  }
}

function LinkPreviewCard({ url, title, description, image, postId }) {
  const [showModal, setShowModal] = useState(false);
  const isMobile = typeof window !== "undefined" && window.matchMedia("(max-width: 900px)").matches;

  let hostname = url;
  try { hostname = new URL(url).hostname; } catch {}

  function openModal() {
    window.history.pushState({ linkPreview: true }, "");
    setShowModal(true);
  }

  function closeModal() { setShowModal(false); }

  useEffect(() => {
    if (!showModal) return;
    const onPop = () => setShowModal(false);
    window.addEventListener("popstate", onPop);
    return () => window.removeEventListener("popstate", onPop);
  }, [showModal]);

  function handleClick(e) {
    e.stopPropagation();
    if (isMobile) {
      e.preventDefault();
      openModal();
    }
  }

  return (
    <>
      <a
        href={url}
        target={isMobile ? "_self" : "_blank"}
        rel="noopener noreferrer"
        style={{ textDecoration: "none", display: "block", marginTop: 10 }}
        onClick={handleClick}
      >
        <div style={{
          border: "1px solid rgba(148,163,184,0.15)",
          borderRadius: 12,
          overflow: "hidden",
          background: "#1a1d27",
          display: "flex",
          alignItems: "stretch",
          gap: 0
        }}>
          <div style={{ flex: 1, padding: "16px 14px", minWidth: 0, display: "flex", flexDirection: "column", justifyContent: "center", textAlign: "left" }}>
            {title && <div style={{ color: "#f1f5f9", fontWeight: 700, fontSize: 16, marginBottom: 6, lineHeight: 1.35 }}>{title}</div>}
            {description && <div style={{ color: "#64748b", fontSize: 12, marginBottom: 8, display: "-webkit-box", WebkitLineClamp: 3, WebkitBoxOrient: "vertical", overflow: "hidden", lineHeight: 1.4 }}>{description}</div>}
            <div style={{ color: "#c084fc", fontSize: 11, fontWeight: 700, letterSpacing: "0.03em", textTransform: "uppercase" }}>{hostname}</div>
          </div>
          {image && (
            <div style={{ width: 100, flexShrink: 0, position: "relative", overflow: "hidden" }}>
              <img
                src={image}
                alt=""
                style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover" }}
                onError={(e) => { e.target.parentElement.style.display = "none"; }}
              />
            </div>
          )}
        </div>
      </a>

      {showModal && (
        <div
          style={{ position: "fixed", inset: 0, zIndex: 9999, display: "flex", flexDirection: "column", justifyContent: "flex-end" }}
          onClick={closeModal}
        >
          <div style={{ position: "absolute", inset: 0, background: "rgba(0,0,0,0.6)" }} />
          <div
            style={{ position: "relative", background: "#1a1d27", borderRadius: "20px 20px 0 0", maxHeight: "80vh", display: "flex", flexDirection: "column" }}
            onClick={(e) => e.stopPropagation()}
          >
            <div style={{ display: "flex", alignItems: "center", padding: "20px 20px 14px", flexShrink: 0 }}>
              <button
                type="button"
                onClick={closeModal}
                style={{ display: "inline-flex", alignItems: "center", justifyContent: "center", width: 26, height: 26, borderRadius: 999, border: "none", background: "#20262f", color: "#dbe4ee", fontSize: 12, fontWeight: 800, cursor: "pointer", flexShrink: 0 }}
              >
                ←
              </button>
            </div>
            <div style={{ overflowY: "auto", padding: "0 20px 36px" }}>
              {image && (
                <img
                  src={image}
                  alt=""
                  style={{ width: "100%", height: 180, objectFit: "cover", borderRadius: 12, marginBottom: 14, display: "block" }}
                  onError={(e) => { e.target.style.display = "none"; }}
                />
              )}
              {title && <div style={{ color: "#f1f5f9", fontWeight: 700, fontSize: 17, marginBottom: 8, lineHeight: 1.3 }}>{title}</div>}
              {description && <div style={{ color: "#94a3b8", fontSize: 14, marginBottom: 10, lineHeight: 1.55 }}>{description}</div>}
              <div style={{ color: "#c084fc", fontSize: 11, fontWeight: 700, marginBottom: 16, textTransform: "uppercase", letterSpacing: "0.04em" }}>{hostname}</div>
              <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                <a
                  href={url}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ display: "block", textAlign: "center", padding: "13px", borderRadius: 12, background: "#c084fc", color: "#14081d", fontWeight: 700, fontSize: 15, textDecoration: "none" }}
                >
                  Open Link
                </a>
                {postId && (
                  <Link
                    to={`/post/${postId}`}
                    onClick={closeModal}
                    style={{ display: "block", textAlign: "center", padding: "13px", borderRadius: 12, background: "#20262f", color: "#dbe4ee", fontWeight: 700, fontSize: 15, textDecoration: "none" }}
                  >
                    Open Post
                  </Link>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

function PostPreviewCard({ postId, title, text, image }) {
  const isMobile = typeof window !== "undefined" && window.matchMedia("(max-width: 900px)").matches;
  const [showModal, setShowModal] = useState(false);
  const PREVIEW_LIMIT = 160;
  const snippet = text && text.length > PREVIEW_LIMIT ? text.slice(0, PREVIEW_LIMIT) + "…" : text;

  function openModal(e) {
    e.preventDefault();
    e.stopPropagation();
    window.history.pushState({ postPreview: true }, "");
    setShowModal(true);
  }
  function closeModal() { setShowModal(false); }

  useEffect(() => {
    if (!showModal) return;
    const onPop = () => setShowModal(false);
    window.addEventListener("popstate", onPop);
    return () => window.removeEventListener("popstate", onPop);
  }, [showModal]);

  return (
    <>
      <Link
        to={`/post/${postId}`}
        style={{ textDecoration: "none", display: "block", marginTop: 10 }}
        onClick={isMobile ? openModal : undefined}
      >
        <div style={{
          border: "1px solid rgba(148,163,184,0.15)",
          borderRadius: 12,
          overflow: "hidden",
          background: "#1a1d27",
          display: "flex",
          alignItems: "stretch",
        }}>
          <div style={{ flex: 1, padding: "16px 14px", minWidth: 0, display: "flex", flexDirection: "column", justifyContent: "center", textAlign: "left" }}>
            {title && <div style={{ color: "#f1f5f9", fontWeight: 700, fontSize: 16, marginBottom: snippet ? 6 : 0, lineHeight: 1.35 }}>{title}</div>}
            {snippet && <div style={{ color: "#64748b", fontSize: 12, marginBottom: 8, lineHeight: 1.4 }}>{snippet}</div>}
            <div style={{ color: "#c084fc", fontSize: 11, fontWeight: 700, letterSpacing: "0.03em", textTransform: "uppercase" }}>View Post →</div>
          </div>
          {image && (
            <div style={{ width: 100, flexShrink: 0, position: "relative", overflow: "hidden" }}>
              <img
                src={image}
                alt=""
                style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover" }}
                onError={(e) => { e.target.parentElement.style.display = "none"; }}
              />
            </div>
          )}
        </div>
      </Link>

      {showModal && (
        <div
          style={{ position: "fixed", inset: 0, zIndex: 9999, display: "flex", flexDirection: "column", justifyContent: "flex-end" }}
          onClick={closeModal}
        >
          <div style={{ position: "absolute", inset: 0, background: "rgba(0,0,0,0.6)" }} />
          <div
            style={{ position: "relative", background: "#1a1d27", borderRadius: "20px 20px 0 0", maxHeight: "80vh", display: "flex", flexDirection: "column" }}
            onClick={(e) => e.stopPropagation()}
          >
            <div style={{ display: "flex", alignItems: "center", padding: "20px 20px 14px", flexShrink: 0 }}>
              <button
                type="button"
                onClick={closeModal}
                style={{ display: "inline-flex", alignItems: "center", justifyContent: "center", width: 26, height: 26, borderRadius: 999, border: "none", background: "#20262f", color: "#dbe4ee", fontSize: 12, fontWeight: 800, cursor: "pointer", flexShrink: 0 }}
              >
                ←
              </button>
            </div>
            <div style={{ overflowY: "auto", padding: "0 20px 36px" }}>
              {image && (
                <img
                  src={image}
                  alt=""
                  style={{ width: "100%", height: 180, objectFit: "cover", borderRadius: 12, marginBottom: 14, display: "block" }}
                  onError={(e) => { e.target.style.display = "none"; }}
                />
              )}
              {title && <div style={{ color: "#f1f5f9", fontWeight: 700, fontSize: 17, marginBottom: 8, lineHeight: 1.3 }}>{title}</div>}
              {text && <div style={{ color: "#94a3b8", fontSize: 14, marginBottom: 10, lineHeight: 1.55, whiteSpace: "pre-wrap" }}>{text}</div>}
              <Link
                to={`/post/${postId}`}
                onClick={closeModal}
                style={{ display: "block", textAlign: "center", padding: "13px", borderRadius: 12, background: "#c084fc", color: "#14081d", fontWeight: 700, fontSize: 15, textDecoration: "none" }}
              >
                View Post
              </Link>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

function PostAttachment({ attachment, postId }) {
  if (!attachment) return null;
  const { type, url, title, description, image } = attachment;

  if (type === "image") {
    return (
      <div style={{ marginTop: 10 }}>
        <img
          src={url}
          alt=""
          style={{ maxWidth: "100%", borderRadius: 10, display: "block", maxHeight: 400, objectFit: "cover" }}
          onError={(e) => { e.target.style.display = "none"; }}
        />
      </div>
    );
  }

  if (type === "video") {
    const isYoutube = /youtube\.com|youtu\.be/.test(url);
    if (isYoutube) {
      const videoId = url.match(/(?:v=|youtu\.be\/)([^&?/]+)/)?.[1];
      return videoId ? (
        <div style={{ marginTop: 10, borderRadius: 10, overflow: "hidden", aspectRatio: "16/9" }}>
          <iframe
            src={`https://www.youtube.com/embed/${videoId}`}
            style={{ width: "100%", height: "100%", border: "none" }}
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          />
        </div>
      ) : null;
    }
    return (
      <div style={{ marginTop: 10 }}>
        <video
          src={url}
          controls
          style={{ maxWidth: "100%", borderRadius: 10, maxHeight: 400 }}
        />
      </div>
    );
  }

  if (type === "link") {
    return <LinkPreviewCard url={url} title={title} description={description} image={image} postId={postId} />;
  }

  return null;
}

function PostCard({ post, commentCount = 0, score = 0, myVote = 0, onVote, showActivity = false }) {
  const [shareLabel, setShareLabel] = useState("Share");
  const [expanded, setExpanded] = useState(false);
  const isMod = isModPost(post);
  const boardName = getBoardNameFromPost(post);
  const { text: postText, attachment } = parsePostContent(post.content);
  const isLong = postText.length > POST_PREVIEW_LIMIT;

  async function handleShare(event) {
    event.preventDefault();
    event.stopPropagation();

    const shareUrl = `${window.location.origin}/post/${post.id}`;

    try {
      if (navigator.share) {
        await navigator.share({
          title: post.title,
          text: post.title,
          url: shareUrl
        });
        setShareLabel("Shared");
      } else if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(shareUrl);
        setShareLabel("Copied");
      } else {
        setShareLabel("Link ready");
      }
    } catch (error) {
      if (error?.name !== "AbortError") {
        setShareLabel("Share failed");
      }
      return;
    }

    window.setTimeout(() => {
      setShareLabel("Share");
    }, 1800);
  }

  const boardSlug = BOARDS.find((b) => b.name === boardName)?.slug;

  return (
    <div className="content-card feed-post-card" style={{ marginBottom: 16 }}>
      <div className="feed-post-board-row" style={{ marginBottom: 10 }}>
        <span className="feed-post-board-group" style={{ flexWrap: "wrap", gap: 5 }}>
          <UserPill
            record={post}
            name={post.username || `Anon #${shortId(post.browser_id)}`}
            color={getUserColor(post.browser_id, post.username)}
          />
          {boardName && (boardSlug ? (
            <Link to={`/board/${boardSlug}`} onClick={(e) => e.stopPropagation()} style={{ textDecoration: "none" }}>
              <BoardBadge boardName={boardName} small />
            </Link>
          ) : (
            <BoardBadge boardName={boardName} small />
          ))}
          {(post.country || post.continent) && (
            <GeoBadge country={post.country} continent={post.continent} small />
          )}
          {(post.pinned || post.locked) && (
            <span className="feed-post-statuses">
              {post.pinned && <span className="feed-post-status" style={{ color: "#f8fafc" }}>📌</span>}
              {post.locked && <span className="feed-post-status" style={{ color: "#f87171" }}>🔒</span>}
            </span>
          )}
        </span>
        <span className="feed-post-time">
          {showActivity ? `Active ${timeAgo(post.last_activity || post.created_at)}` : timeAgo(post.created_at)}
        </span>
      </div>

      {attachment && attachment.type !== "image" ? (
        <PostAttachment attachment={attachment} postId={post.id} />
      ) : (
        <PostPreviewCard
          postId={post.id}
          title={post.title || null}
          text={postText || null}
          image={attachment?.type === "image" ? attachment.url : null}
        />
      )}

      <div className="feed-post-actions">
        <button
          type="button"
          className="feed-post-action-pill"
          style={myVote === 1 ? { borderColor: "#c084fc", background: "rgba(192,132,252,0.15)" } : {}}
          onClick={(event) => {
            event.preventDefault();
            event.stopPropagation();
            onVote?.(post.id, myVote === 1 ? 0 : 1);
          }}
        >
          <span>👍</span>
          <span>{score}</span>
        </button>

        <Link
          to={`/post/${post.id}`}
          state={{ scrollToComments: true }}
          className="feed-post-action-pill"
        >
          <span>💬</span>
          <span>{commentCount}</span>
        </Link>

        <button
          type="button"
          className="feed-post-action-pill"
          onClick={handleShare}
        >
          <span>↗</span>
          <span>{shareLabel}</span>
        </button>
      </div>
    </div>
  );
}

function SearchBar() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [query, setQuery] = useState(searchParams.get("q") || "");
  const [focused, setFocused] = useState(false);
  const [pickedContinent, setPickedContinent] = useState(null);
  const inputRef = useRef(null);
  const shellRef = useRef(null);
  const searchParamsRef = useRef(searchParams);
  useEffect(() => { searchParamsRef.current = searchParams; }, [searchParams]);

  const boardTag = searchParams.get("board") || "";
  const continentTag = searchParams.get("continent") || "";
  const countryTag = searchParams.get("country") || "";

  // Debounce text query into URL param
  useEffect(() => {
    const t = setTimeout(() => {
      const p = new URLSearchParams(searchParamsRef.current);
      if (query.trim()) p.set("q", query.trim()); else p.delete("q");
      setSearchParams(p, { replace: true });
    }, 300);
    return () => clearTimeout(t);
  }, [query]);

  // Close dropdown on outside click
  useEffect(() => {
    function onMouseDown(e) {
      if (shellRef.current && !shellRef.current.contains(e.target)) { setFocused(false); setPickedContinent(null); }
    }
    document.addEventListener("mousedown", onMouseDown);
    return () => document.removeEventListener("mousedown", onMouseDown);
  }, []);

  const q = query.toLowerCase().trim();
  const boardSuggestions = BOARDS.filter(b => b.slug !== boardTag && (q ? b.name.toLowerCase().includes(q) : true));
  const continentSuggestions = CONTINENTS.filter(c => c !== continentTag && (q ? c.toLowerCase().includes(q) : true));
  const countrySearchSuggestions = q
    ? COUNTRIES_WITH_FLAGS.filter(c => c.name !== countryTag && c.name.toLowerCase().includes(q)).slice(0, 8)
    : [];
  const countriesInContinent = pickedContinent
    ? COUNTRIES_WITH_FLAGS.filter(c => COUNTRY_CONTINENT[c.name] === pickedContinent)
    : [];

  const isCountryPickerMode = !!pickedContinent;
  const showBoardSection = !isCountryPickerMode && boardSuggestions.length > 0;
  const showContinentSection = !isCountryPickerMode && continentSuggestions.length > 0;
  const showCountrySearchSection = !isCountryPickerMode && countrySearchSuggestions.length > 0;
  const showDropdown = focused && (isCountryPickerMode || showBoardSection || showContinentSection || showCountrySearchSection);

  function addBoard(slug) {
    const p = new URLSearchParams(searchParams); p.set("board", slug);
    setSearchParams(p); setQuery(""); setFocused(false); setPickedContinent(null);
  }
  function addContinent(c) {
    const p = new URLSearchParams(searchParams); p.set("continent", c); p.delete("country");
    setSearchParams(p); setQuery("");
  }
  function pickContinent(c) {
    setPickedContinent(c); setQuery("");
  }
  function addCountry(name) {
    const p = new URLSearchParams(searchParams); p.set("country", name); p.delete("continent");
    setSearchParams(p); setQuery(""); setFocused(false); setPickedContinent(null);
  }
  function removeBoard() {
    const p = new URLSearchParams(searchParams); p.delete("board"); setSearchParams(p);
  }
  function removeContinent() {
    const p = new URLSearchParams(searchParams); p.delete("continent"); setSearchParams(p);
  }
  function removeCountry() {
    const p = new URLSearchParams(searchParams); p.delete("country"); setSearchParams(p);
  }
  function clearQuery() {
    setQuery("");
    const p = new URLSearchParams(searchParams); p.delete("q"); setSearchParams(p, { replace: true });
  }

  const boardObj = BOARDS.find(b => b.slug === boardTag);
  const hasAnyTag = boardTag || continentTag || countryTag;

  return (
    <div className="search-shell" ref={shellRef}>
      <div className="search-bar-wrap">
        <div className={`search-bar${focused ? " focused" : ""}`} onClick={() => inputRef.current?.focus()}>
          <span className="search-icon">🔍</span>
          {boardObj && (
            <span className="search-chip board-chip">
              <span>{boardObj.icon}</span>
              <span>{boardObj.name}</span>
              <button type="button" onClick={e => { e.stopPropagation(); removeBoard(); }}>×</button>
            </span>
          )}
          {continentTag && (
            <span className="search-chip continent-chip">
              <span>{CONTINENT_GLOBE[continentTag] || "🌐"}</span>
              <span>{continentTag}</span>
              <button type="button" onClick={e => { e.stopPropagation(); removeContinent(); }}>×</button>
            </span>
          )}
          {countryTag && (
            <span className="search-chip country-chip">
              <span>{getCountryFlag(countryTag)} {countryTag}</span>
              <button type="button" onClick={e => { e.stopPropagation(); removeCountry(); }}>×</button>
            </span>
          )}
          <input
            ref={inputRef}
            className="search-input"
            value={query}
            onChange={e => { setQuery(e.target.value); setPickedContinent(null); }}
            onFocus={() => setFocused(true)}
            onKeyDown={e => { if (e.key === "Escape") { setFocused(false); setPickedContinent(null); } }}
            placeholder={!hasAnyTag ? "Search or filter by board, region, country…" : "Add keywords to filter…"}
          />
          {query && <button className="search-clear" type="button" onClick={e => { e.stopPropagation(); clearQuery(); }}>×</button>}
        </div>

        {showDropdown && (
          <div className="search-dropdown">
            <button
              type="button"
              onClick={() => { setFocused(false); setPickedContinent(null); }}
              style={{ position: "absolute", top: 8, left: 8, display: "flex", alignItems: "center", justifyContent: "center", width: 22, height: 22, borderRadius: 999, border: "none", background: "#2d2f3a", color: "#94a3b8", fontSize: 14, lineHeight: 1, cursor: "pointer", padding: 0 }}
            >×</button>

            {isCountryPickerMode ? (
              <>
                <div className="search-section-label" style={{ paddingLeft: 32 }}>
                  <button type="button" onClick={() => setPickedContinent(null)} style={{ background: "none", border: "none", color: "#c084fc", fontSize: 11, fontWeight: 700, cursor: "pointer", padding: 0, marginRight: 4 }}>← Back</button>
                  {pickedContinent}
                </div>
                {countriesInContinent.map(c => (
                  <button key={c.name} className="search-suggestion" type="button" onClick={() => addCountry(c.name)}>
                    <span className="sugg-icon">{c.flag}</span>
                    <span className="sugg-label">{c.name}</span>
                  </button>
                ))}
              </>
            ) : (
              <>
                {(showBoardSection || showContinentSection) && (
                  <div className="search-columns">
                    {showBoardSection && (
                      <div className="search-column">
                        <div className="search-section-label">Boards</div>
                        {boardSuggestions.map(b => (
                          <button key={b.slug} className="search-suggestion" type="button" onClick={() => addBoard(b.slug)}>
                            <span className="sugg-icon">{b.icon}</span>
                            <span className="sugg-label">{b.name}</span>
                          </button>
                        ))}
                      </div>
                    )}
                    {showContinentSection && (
                      <div className="search-column">
                        <div className="search-section-label">Regions</div>
                        {continentSuggestions.map(c => (
                          <button key={c} className="search-suggestion" type="button"
                            onClick={() => { addContinent(c); pickContinent(c); }}>
                            <span className="sugg-icon">🌍</span>
                            <span className="sugg-label">{c}</span>
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                )}
                {showCountrySearchSection && (
                  <>
                    {(showBoardSection || showContinentSection) && <div className="search-divider" />}
                    <div className="search-section-label">Countries</div>
                    {countrySearchSuggestions.map(c => (
                      <button key={c.name} className="search-suggestion" type="button" onClick={() => addCountry(c.name)}>
                        <span className="sugg-icon">{c.flag}</span>
                        <span className="sugg-label">{c.name}</span>
                      </button>
                    ))}
                  </>
                )}
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function CommentCard({ comment, postBrowserId, postUsername, canDelete = false, onDelete, onReply, allComments = [], threadReplies = [] }) {
  const isModUser = isModPost(comment);
  const [isReplying, setIsReplying] = useState(false);
  const [replyText, setReplyText] = useState("");
  const [isSendingReply, setIsSendingReply] = useState(false);
  const [repliesExpanded, setRepliesExpanded] = useState(false);
  const [quoteExpanded, setQuoteExpanded] = useState(false);
  const isPending = comment.isPending === true;
  const displayName =
    isPending && !isModUser && !comment.username
      ? "Anonymous"
      : (comment.username || `Anon #${shortId(comment.browser_id)}`);

  const avatarColor = isModUser ? "#c084fc" : getUserColor(comment.browser_id, comment.username);
  const roleBadge = getRoleBadge(comment);
  const avatarLetter = roleBadge || (displayName[0]?.toUpperCase() || "?");

  const parentComment = comment.parent_comment_id
    ? allComments.find((c) => c.id === comment.parent_comment_id)
    : null;
  const parentName = parentComment
    ? (parentComment.username || `Anon #${shortId(parentComment.browser_id)}`)
    : null;
  // Only show quote when replying to a reply (not for direct replies to a top-level comment)
  const showQuote = parentComment && !!parentComment.parent_comment_id;

  return (
    <div className="comment-flat">
      <div className="comment-card">
        <div className="comment-card-header">
          <UserPill record={comment} name={displayName} color={avatarColor} />
          {comment.browser_id === postBrowserId &&
            (postUsername ? comment.username === postUsername : !comment.username) && (
            <span className="comment-card-op">OP</span>
          )}
          <span className="comment-card-time">· {timeAgo(comment.created_at)}</span>
        </div>

        {showQuote && (
          <div className="comment-quote" onClick={() => setQuoteExpanded((v) => !v)} style={{ cursor: "pointer" }}>
            <span className="comment-quote-author">{parentName}:</span>
            <p className="comment-quote-body" style={quoteExpanded ? { display: "block", WebkitLineClamp: "unset" } : {}}>{parentComment.content}</p>
            {!quoteExpanded && parentComment.content.length > 120 && (
              <span style={{ fontSize: 11, color: "#c084fc", fontWeight: 700 }}>Show more</span>
            )}
          </div>
        )}

        <div className="comment-body">{comment.content}</div>

        <div className="comment-footer-actions">
          {onReply && (
            <button
              type="button"
              className="comment-header-btn"
              onClick={() => {
                setIsReplying((v) => !v);
                setRepliesExpanded(true);
              }}
            >
              Reply
            </button>
          )}
          {threadReplies.length > 0 && (
            <button
              type="button"
              className="comment-header-btn"
              onClick={() => setRepliesExpanded((v) => !v)}
            >
              {repliesExpanded ? "▲" : "▼"} {threadReplies.length} {threadReplies.length === 1 ? "Reply" : "Replies"}
            </button>
          )}
          {canDelete && (
            <button type="button" className="comment-header-btn" onClick={onDelete}>
              🗑
            </button>
          )}
        </div>

        {isReplying && (
          <div className="inline-reply-box">
            <textarea
              className="comment-composer-textarea"
              placeholder={`Reply to ${displayName}...`}
              value={replyText}
              onChange={(e) => setReplyText(e.target.value)}
              disabled={isSendingReply}
              rows={3}
              autoFocus
            />
            <div className="comment-composer-actions">
              <button
                type="button"
                className="comment-composer-cancel"
                onClick={() => { setIsReplying(false); setReplyText(""); }}
              >
                Cancel
              </button>
              <button
                type="button"
                className="comment-composer-submit"
                disabled={isSendingReply}
                onClick={async () => {
                  if (!replyText.trim()) return;
                  setIsSendingReply(true);
                  await onReply(replyText, comment.id);
                  setIsSendingReply(false);
                  setIsReplying(false);
                  setReplyText("");
                }}
              >
                Comment
              </button>
            </div>
          </div>
        )}

        {repliesExpanded && threadReplies.length > 0 && (
          <div className="comment-replies-list">
            {threadReplies.map((r) => (
              <CommentCard
                key={r.id}
                comment={r}
                postBrowserId={postBrowserId}
                canDelete={canDelete}
                onDelete={onDelete ? () => onDelete(r.id) : undefined}
                onReply={onReply}
                allComments={allComments}
                threadReplies={[]}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function ChatMessage({ comment, postBrowserId, postUsername, canDelete, onDelete, canPin, onPin, onReply, onReact, reactions = {}, allComments = [], onFindParent }) {
  const isModUser = isModPost(comment);
  const isPending = comment.isPending === true;
  const displayName = isPending && !isModUser && !comment.username
    ? "Anonymous"
    : (comment.username || `Anon #${shortId(comment.browser_id)}`);
  const avatarColor = isModUser ? "#c084fc" : getUserColor(comment.browser_id, comment.username);
  const roleBadge2 = getRoleBadge(comment);
  const avatarLetter = roleBadge2 || (displayName[0]?.toUpperCase() || "?");
  const isOP = comment.browser_id === postBrowserId &&
    (postUsername ? comment.username === postUsername : !comment.username);
  const [showActions, setShowActions] = useState(false);
  const [isPickingEmoji, setIsPickingEmoji] = useState(false);
  const emojiInputRef = useRef(null);
  const myId = getBrowserId();

  const parentComment = comment.parent_comment_id
    ? allComments.find((c) => c.id === comment.parent_comment_id)
    : null;
  const parentName = parentComment
    ? (parentComment.username || `Anon #${shortId(parentComment.browser_id)}`)
    : null;

  const commentReactions = reactions[comment.id] || {};
  const reactionEntries = Object.entries(commentReactions);

  function handleReactClick() {
    setShowActions(false);
    setIsPickingEmoji(true);
    if (emojiInputRef.current) {
      emojiInputRef.current.value = "";
      emojiInputRef.current.focus();
    }
  }

  function handleEmojiInput(e) {
    const val = e.target.value;
    const chars = [...val];
    const emoji = chars.find((c) => /\p{Emoji}/u.test(c) && c !== "\u200d");
    if (emoji) {
      onReact && onReact(comment.id, emoji);
      e.target.value = "";
      setIsPickingEmoji(false);
    }
  }

  return (
    <div className="chat-msg" data-comment-id={comment.id}>
      <div className="chat-msg-body">
        <div className="chat-msg-meta">
          <UserPill record={comment} name={displayName} color={avatarColor} />
          {isOP && <span className="comment-card-op">OP</span>}
          {comment.pinned && <span style={{ fontSize: 10, fontWeight: 600, color: "#c084fc", letterSpacing: "0.03em" }}>📌 pinned</span>}
          <span className="chat-msg-time">· {timeAgo(comment.created_at)}</span>
        </div>
        {showActions && (
          <div className="chat-action-sheet">
            <button
              type="button"
              className="chat-action-btn"
              onClick={() => { setShowActions(false); onReply && onReply(comment); }}
            >
              Reply
            </button>
            <button
              type="button"
              className="chat-action-btn"
              onClick={handleReactClick}
            >
              React
            </button>
            {comment.parent_comment_id && (
              <button
                type="button"
                className="chat-action-btn"
                onClick={() => { setShowActions(false); onFindParent && onFindParent(comment.parent_comment_id); }}
              >
                Find
              </button>
            )}
            {canPin && (
              <button
                type="button"
                className="chat-action-btn"
                onClick={(e) => { e.stopPropagation(); setShowActions(false); onPin && onPin(); }}
              >
                {comment.pinned ? "Unpin" : "📌 Pin"}
              </button>
            )}
            {canDelete && (
              <button
                type="button"
                className="chat-action-btn"
                onClick={(e) => { e.stopPropagation(); setShowActions(false); onDelete(); }}
              >
                Delete
              </button>
            )}
          </div>
        )}

        {(() => {
          const { text: msgText, attachment: msgAttachment } = parsePostContent(comment.content);
          const { text: parentText } = parentComment ? parsePostContent(parentComment.content) : {};
          return (
            <div
              className={`chat-bubble${isPending ? " pending" : ""}`}
              onClick={() => !isPending && setShowActions((v) => !v)}
              style={comment.pinned ? { borderLeft: "2px solid rgba(192,132,252,0.5)", background: "rgba(192,132,252,0.06)", paddingLeft: 10 } : undefined}
            >
              {parentComment && (
                <div className="chat-quote-bar">
                  <span className="chat-quote-name">{parentName}</span>
                  <p className="chat-quote-text">{parentText || parentComment.content}</p>
                </div>
              )}
              {msgText && <span className="chat-bubble-text">{msgText}</span>}
              {msgAttachment && (
                <div style={{ marginTop: msgText ? 6 : 0 }} onClick={(e) => e.stopPropagation()}>
                  <PostAttachment attachment={msgAttachment} />
                </div>
              )}
            </div>
          );
        })()}

        {reactionEntries.length > 0 && (
          <div className="chat-reactions">
            {reactionEntries.map(([emoji, voters]) => (
              <button
                key={emoji}
                type="button"
                className={`chat-reaction-pill${voters.includes(myId) ? " mine" : ""}`}
                onClick={() => onReact && onReact(comment.id, emoji)}
              >
                {emoji}
                <span className="chat-reaction-count">{voters.length}</span>
              </button>
            ))}
          </div>
        )}

        <div className="chat-emoji-picker-row" style={{ display: isPickingEmoji ? "" : "none" }}>
          <input
            ref={emojiInputRef}
            className="chat-emoji-picker-input"
            type="text"
            inputMode="emoji"
            placeholder="Pick an emoji..."
            onChange={handleEmojiInput}
            onBlur={() => setIsPickingEmoji(false)}
          />
        </div>
      </div>
    </div>
  );
}

// ==============================
// MOD ACTION
// ==============================
async function modAction(action) {
  try {
    const headers = getAuthHeader();

    const res = await fetch("https://daboysforumip.coldbrainarchive.workers.dev/mod-action", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...headers
      },
      body: JSON.stringify(action)
    });

    const data = await res.json();
    if (!res.ok) alert(data.error);
  } catch (err) {
    alert(err.message);
  }
}

// ==============================
// AUTH
// ==============================
function Auth({ setUser }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const signIn = async () => {
    try {
      const res = await fetch(`${WORKER_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username.trim(), password })
      });
      const data = await res.json();
      if (!res.ok) { alert(data.error || "Login failed"); return; }
      localStorage.setItem("auth_token", data.token);
      localStorage.setItem("auth_user", JSON.stringify(data.user));
      if ((data.user.role === "mod" || data.user.role === "admin") && data.user.username) {
        localStorage.setItem("mod_name", data.user.username);
      }
      setUser(data.user);
    } catch (err) { alert(err.message); }
  };

  return (
    <div
      style={{
        maxWidth: 520,
        margin: "32px auto",
        padding: 24,
        border: "1px solid #2e303a",
        borderRadius: 18,
        background: "linear-gradient(180deg, #1b1d24 0%, #14161c 100%)",
        boxShadow: "0 18px 50px rgba(0, 0, 0, 0.35)",
        textAlign: "left"
      }}
    >
      <h2 style={{ marginBottom: 16 }}>Login</h2>

      <div style={{ display: "grid", gap: 12 }}>
        <input
          onChange={(e) => setUsername(e.target.value)}
          placeholder="username"
          style={{
            width: "100%",
            boxSizing: "border-box",
            padding: "14px 16px",
            borderRadius: 12,
            border: "1px solid #3f4756",
            fontSize: 16,
            background: "#0f1117",
            color: "#f8fafc"
          }}
        />
        <input
          type="password"
          onChange={(e) => setPassword(e.target.value)}
          placeholder="password"
          onKeyDown={(e) => e.key === "Enter" && signIn()}
          style={{
            width: "100%",
            boxSizing: "border-box",
            padding: "14px 16px",
            borderRadius: 12,
            border: "1px solid #3f4756",
            fontSize: 16,
            background: "#0f1117",
            color: "#f8fafc"
          }}
        />
        <button
          onClick={signIn}
          style={{
            width: "100%",
            padding: "14px 18px",
            borderRadius: 14,
            border: "none",
            background: "#c084fc",
            color: "#14081d",
            fontWeight: 700,
            fontSize: 15,
            cursor: "pointer",
            boxShadow: "0 14px 30px rgba(192, 132, 252, 0.28)"
          }}
        >
          Login
        </button>
      </div>
    </div>
  );
}

// ==============================
// HOME
// ==============================
function Home() {
  const [posts, setPosts] = useState([]);
  const [commentCounts, setCommentCounts] = useState({});
  const [voteData, setVoteData] = useState({});
  const [displayCount, setDisplayCount] = useState(10);
  const sentinelRef = useRef(null);
  const [searchParams] = useSearchParams();
  const boardFilter = searchParams.get("board") || "";
  const continentFilter = searchParams.get("continent") || "";
  const countryFilter = searchParams.get("country") || "";
  const textQuery = (searchParams.get("q") || "").toLowerCase().trim();
  const scrollRestoredRef = useRef(false);
  const scrollKey = "scroll:/";

  useEffect(() => {
    const onScroll = () => {
      if (scrollRestoredRef.current) sessionStorage.setItem(scrollKey, String(window.scrollY));
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    if (scrollRestoredRef.current || posts.length === 0) return;
    scrollRestoredRef.current = true;
    const saved = sessionStorage.getItem(scrollKey);
    if (saved) requestAnimationFrame(() => requestAnimationFrame(() => window.scrollTo(0, parseInt(saved, 10))));
  }, [posts]);

  const fetchPosts = useCallback(async () => {
    const [postsRes, commentsRes] = await Promise.all([
      fetch(`${WORKER_URL}/get-posts?limit=100`),
      fetch(`${WORKER_URL}/get-comments-index`)
    ]);
    const { posts: postsData } = postsRes.ok ? await postsRes.json() : { posts: [] };
    const commentsData = commentsRes.ok ? await commentsRes.json() : [];

    setCommentCounts(countValidComments(commentsData));
    const hydratedPosts = hydratePostsWithBoardTags(
      (postsData || []).filter((p) => {
        const b = getBoardNameFromPost(p);
        return b !== "Cage" && b !== "Jail" && (!p.pinned || p.pinned_global);
      })
    );
    setPosts(hydratedPosts);

    const votes = await fetchVotesForPosts(hydratedPosts.map((p) => p.id));
    setVoteData(votes);
  }, []);

  useEffect(() => {
    const timeoutId = window.setTimeout(() => {
      void fetchPosts();
    }, 0);
    const i = window.setInterval(() => {
      void fetchPosts();
    }, 4000);
    return () => {
      window.clearTimeout(timeoutId);
      window.clearInterval(i);
    };
  }, [fetchPosts]);

  useEffect(() => { setDisplayCount(10); }, [boardFilter, continentFilter, countryFilter, textQuery]);

  useEffect(() => {
    const sentinel = sentinelRef.current;
    if (!sentinel) return;
    const observer = new IntersectionObserver(
      (entries) => { if (entries[0].isIntersecting) setDisplayCount(prev => prev + 10); },
      { rootMargin: "200px" }
    );
    observer.observe(sentinel);
    return () => observer.disconnect();
  });

  const isActivityFilter = boardFilter === "activity";
  const filteredPosts = posts
    .filter(p => {
      if (!boardFilter) return true;
      if (isActivityFilter) {
        const isBot = BOT_USERNAMES.includes(p.username);
        if (!isBot) return true;
        return (commentCounts[p.id] || 0) > 0 || (voteData[p.id]?.voteCount ?? 0) > 0;
      }
      return getBoardNameFromPost(p) === (getBoardBySlug(boardFilter)?.name || boardFilter);
    })
    .filter(p => !continentFilter || p.continent === continentFilter)
    .filter(p => !countryFilter || p.country === countryFilter)
    .filter(p => {
      if (!textQuery) return true;
      const { text, attachment } = parsePostContent(p.content);
      const haystack = [attachment?.title, attachment?.description, attachment?.url, text].filter(Boolean).join(" ").toLowerCase();
      return haystack.includes(textQuery);
    })
    .sort((a, b) => {
      const pinnedDiff = (b.pinned_global ? 1 : 0) - (a.pinned_global ? 1 : 0);
      if (pinnedDiff !== 0) return pinnedDiff;
      if (isActivityFilter) return new Date(b.last_activity || b.created_at) - new Date(a.last_activity || a.created_at);
      return new Date(b.created_at) - new Date(a.created_at);
    });

  return (
    <div className="home-shell">
      <SearchBar />

      <main className="home-feed">
        {filteredPosts.slice(0, displayCount).map((p) => (
          <PostCard
            key={p.id}
            post={p}
            commentCount={commentCounts[p.id] || 0}
            score={voteData[p.id]?.score ?? 0}
            myVote={voteData[p.id]?.myVote ?? 0}
            showActivity={isActivityFilter}
            onVote={async (postId, value) => {
              const result = await voteOnPost(postId, value);
              if (result.success) {
                setVoteData((prev) => ({ ...prev, [postId]: { score: result.score, myVote: result.myVote, voteCount: result.voteCount ?? prev[postId]?.voteCount ?? 0 } }));
              }
            }}
          />
        ))}
        {displayCount < filteredPosts.length && (
          <div ref={sentinelRef} style={{ height: 1 }} />
        )}
      </main>
    </div>
  );
}

function BoardPage() {
  const { slug } = useParams();
  const [posts, setPosts] = useState([]);
  const [commentCounts, setCommentCounts] = useState({});
  const [voteData, setVoteData] = useState({});
  const [displayCount, setDisplayCount] = useState(10);
  const sentinelRef = useRef(null);
  const board = getBoardBySlug(slug);
  const [searchParams] = useSearchParams();
  const continentFilter = searchParams.get("continent") || "";
  const countryFilter = searchParams.get("country") || "";
  const textQuery = (searchParams.get("q") || "").toLowerCase().trim();
  const scrollRestoredRef = useRef(false);
  const scrollKey = `scroll:/board/${slug}`;

  useEffect(() => {
    scrollRestoredRef.current = false;
  }, [slug]);

  useEffect(() => {
    const onScroll = () => {
      if (scrollRestoredRef.current) sessionStorage.setItem(scrollKey, String(window.scrollY));
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, [scrollKey]);

  useEffect(() => {
    if (scrollRestoredRef.current || posts.length === 0) return;
    scrollRestoredRef.current = true;
    const saved = sessionStorage.getItem(scrollKey);
    if (saved) requestAnimationFrame(() => requestAnimationFrame(() => window.scrollTo(0, parseInt(saved, 10))));
  }, [posts, scrollKey]);

  const fetchPosts = useCallback(async () => {
    const [postsRes, commentsRes] = await Promise.all([
      fetch(`${WORKER_URL}/get-posts?limit=100`),
      fetch(`${WORKER_URL}/get-comments-index`)
    ]);
    const { posts: postsData } = postsRes.ok ? await postsRes.json() : { posts: [] };
    const commentsData = commentsRes.ok ? await commentsRes.json() : [];

    setCommentCounts(countValidComments(commentsData));
    const hydratedPosts = hydratePostsWithBoardTags(postsData || []);
    setPosts(hydratedPosts);

    const votes = await fetchVotesForPosts(hydratedPosts.map((p) => p.id));
    setVoteData(votes);
  }, []);

  useEffect(() => {
    const timeoutId = window.setTimeout(() => {
      void fetchPosts();
    }, 0);
    const i = window.setInterval(() => {
      void fetchPosts();
    }, 4000);
    return () => {
      window.clearTimeout(timeoutId);
      window.clearInterval(i);
    };
  }, [fetchPosts, slug]);

  if (!board) {
    return (
      <div className="home-shell">
        <SearchBar />
        <main className="home-feed">
          <div className="content-card">
            <h2 style={{ marginTop: 0 }}>Board not found</h2>
            <p style={{ color: "#cbd5e1" }}>That board doesn’t exist.</p>
          </div>
        </main>
      </div>
    );
  }

  useEffect(() => { setDisplayCount(10); }, [continentFilter, countryFilter, textQuery, slug]);

  useEffect(() => {
    const sentinel = sentinelRef.current;
    if (!sentinel) return;
    const observer = new IntersectionObserver(
      (entries) => { if (entries[0].isIntersecting) setDisplayCount(prev => prev + 10); },
      { rootMargin: "200px" }
    );
    observer.observe(sentinel);
    return () => observer.disconnect();
  });

  const isActivityBoard = slug === "activity";
  const basePosts = (isActivityBoard
    ? posts
        .filter(p => { const b = getBoardNameFromPost(p); return b !== "Cage" && b !== "Jail"; })
        .filter(p => (commentCounts[p.id] || 0) > 0 || (voteData[p.id]?.voteCount ?? 0) > 0)
        .filter(p => !p.pinned || p.pinned_global)
    : filterPostsForBoard(posts, board.name)
  );
  const filteredPosts = basePosts
    .filter(p => !continentFilter || p.continent === continentFilter)
    .filter(p => !countryFilter || p.country === countryFilter)
    .filter(p => {
      if (!textQuery) return true;
      const { text, attachment } = parsePostContent(p.content);
      const haystack = [attachment?.title, attachment?.description, attachment?.url, text].filter(Boolean).join(" ").toLowerCase();
      return haystack.includes(textQuery);
    })
    .sort((a, b) => {
      if (a.pinned_global !== b.pinned_global) return (b.pinned_global ? 1 : 0) - (a.pinned_global ? 1 : 0);
      if (a.pinned !== b.pinned) return (b.pinned ? 1 : 0) - (a.pinned ? 1 : 0);
      if (isActivityBoard) return new Date(b.last_activity || b.created_at) - new Date(a.last_activity || a.created_at);
      return new Date(b.created_at) - new Date(a.created_at);
    });

  return (
    <div className="home-shell">
      <SearchBar />

      <main className="home-feed">
        {filteredPosts.length === 0 && (
          <div className="content-card" style={{ marginBottom: 16 }}>
            <h3 style={{ marginTop: 0, marginBottom: 10 }}>{isActivityBoard ? "No activity yet" : "No threads yet"}</h3>
            <p style={{ color: "#cbd5e1", marginBottom: 0 }}>
              {isActivityBoard ? "Posts that users interact with will appear here." : "This board is empty for now. Start the first thread."}
            </p>
          </div>
        )}

        {filteredPosts.slice(0, displayCount).map((p) => (
          <PostCard
            key={p.id}
            post={p}
            commentCount={commentCounts[p.id] || 0}
            score={voteData[p.id]?.score ?? 0}
            myVote={voteData[p.id]?.myVote ?? 0}
            showActivity={isActivityBoard}
            onVote={async (postId, value) => {
              const result = await voteOnPost(postId, value);
              if (result.success) {
                setVoteData((prev) => ({ ...prev, [postId]: { score: result.score, myVote: result.myVote, voteCount: result.voteCount ?? prev[postId]?.voteCount ?? 0 } }));
              }
            }}
          />
        ))}
        {displayCount < filteredPosts.length && (
          <div ref={sentinelRef} style={{ height: 1 }} />
        )}
      </main>
    </div>
  );
}

// ==============================
// CREATE POST (FIXED)
// ==============================
function NewPost({ user, userRole, memberUsername }) {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [previewName, setPreviewName] = useState(null);
  const [isUserJailed, setIsUserJailed] = useState(false);
  const requestedBoard = getBoardBySlug(searchParams.get("board"));
  const [selectedBoardSlug, setSelectedBoardSlug] = useState(requestedBoard?.slug || "random");
  const [selectedCountry, setSelectedCountry] = useState("");
  const [tagOpen, setTagOpen] = useState(false);
  const [tagPickedContinent, setTagPickedContinent] = useState(null);
  const tagShellRef = useRef(null);
  const [attachment, setAttachment] = useState(null);
  const [attachMode, setAttachMode] = useState(null);
  const [linkInput, setLinkInput] = useState("");
  const [linkLoading, setLinkLoading] = useState(false);
  const [uploadLoading, setUploadLoading] = useState(false);
  const imageInputRef = useRef(null);
  const videoInputRef = useRef(null);

  useEffect(() => {
    function onMouseDown(e) {
      if (tagShellRef.current && !tagShellRef.current.contains(e.target)) { setTagOpen(false); setTagPickedContinent(null); }
    }
    document.addEventListener("mousedown", onMouseDown);
    return () => document.removeEventListener("mousedown", onMouseDown);
  }, []);

  useEffect(() => {
    if (user) {
      if (memberUsername) setPreviewName(memberUsername);
      return;
    }
    const browserId = getBrowserId();
    (async () => {
      const jailRes = await fetch(`${WORKER_URL}/check-jailed?browser_id=${browserId}`);
      const jailData = jailRes.ok ? await jailRes.json() : {};
      if (jailData.jailed) {
        setIsUserJailed(true);
        setSelectedBoardSlug("cage");
      }
      try {
        const res = await fetch("https://daboysforumip.coldbrainarchive.workers.dev/my-username", { headers: getOptionalAuthHeader() });
        if (res.ok) { const d = await res.json(); if (d.username) setPreviewName(d.username); }
      } catch {}
    })();
  }, [user, memberUsername]);

  async function handleFileUpload(file, type) {
    setUploadLoading(true);
    try {
      const formData = new FormData();
      formData.append("file", file);
      const res = await fetch(`${WORKER_URL}/upload`, { method: "POST", body: formData });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Upload failed");
      setAttachment({ type, url: data.url });
      setAttachMode(null);
    } catch (err) {
      alert("Upload failed: " + err.message);
    } finally {
      setUploadLoading(false);
    }
  }

  async function handleAddLink() {
    if (!linkInput.trim()) return;
    let url = linkInput.trim();
    if (!/^https?:\/\//i.test(url)) url = "https://" + url;
    setLinkLoading(true);
    try {
      const res = await fetch(`https://api.microlink.io/?url=${encodeURIComponent(url)}`);
      const data = await res.json();
      const d = data.data || {};
      setAttachment({ type: "link", url: d.url || url, title: d.title, description: d.description, image: d.image?.url });
    } catch {
      setAttachment({ type: "link", url });
    } finally {
      setLinkLoading(false);
      setAttachMode(null);
      setLinkInput("");
    }
  }

  const createPost = async () => {
    try {
      if (!title.trim()) return alert("Give your post a title");
      if (!content.trim() && !attachment) return alert("Add a body, or attach a link, photo, or video");
      if (isSending) return;
      if (isUserJailed && selectedBoardSlug !== "cage") {
        return alert("🪹 You are caged — you can only post in the Cage board");
      }

      setIsSending(true);

      const modMetadata = buildModMetadata(getStoredUser(), memberUsername);
      const authHeaders = getOptionalAuthHeader();
      const selectedBoard = getBoardBySlug(selectedBoardSlug) || BOARDS[0];
      const browserId = getBrowserId();

      const res = await fetch("https://daboysforumip.coldbrainarchive.workers.dev/create-post", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...authHeaders
        },
        body: JSON.stringify({
          title,
          content: attachment ? content + ATTACH_MARKER + JSON.stringify(attachment) + "]" : content,
          board: selectedBoard.name,
          category: selectedBoard.name,
          community_id: selectedBoard.slug,
          continent: null,
          country: selectedCountry || null,
          browser_id: browserId,
          ...modMetadata
        })
      });

      const result = await res.json();
      if (!res.ok) {
        setIsSending(false);
        if (result.error === "Banned") {
          alert("🚫 You are banned from posting");
        } else {
          alert(result.error);
        }
        return;
      }

      if (user && memberUsername) {
        fetch(`${WORKER_URL}/backfill-username`, {
          method: "POST",
          headers: { "Content-Type": "application/json", ...getOptionalAuthHeader() },
          body: JSON.stringify({ browser_id: browserId, username: memberUsername })
        }).catch(() => {});
      }

      queuePendingBoardTag({
        title,
        content,
        browserId,
        boardName: selectedBoard.name
      });
      syncBoardTagToPostRecord({ postId: result.post?.id, board: selectedBoard });

      setTitle("");
      setContent("");
      setIsSending(false);
      navigate("/");
    } catch (err) {
      setIsSending(false);
      alert(err.message);
    }
  };

  const selectedBoard = getBoardBySlug(selectedBoardSlug) || BOARDS[0];

  return (
    <div className="home-shell">
      <main className="home-feed" style={{ textAlign: "left", marginTop: 16 }}>

        <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 12 }}>
          <button
            type="button"
            onClick={() => navigate(-1)}
            style={{ display: "inline-flex", alignItems: "center", justifyContent: "center", width: 26, height: 26, borderRadius: 999, border: "none", background: "#20262f", color: "#dbe4ee", fontSize: 12, fontWeight: 800, cursor: "pointer", flexShrink: 0 }}
          >←</button>
          <span style={{ fontSize: 13, fontWeight: 600, color: "#94a3b8" }}>New post</span>
        </div>

        <div className="content-card feed-post-card" style={{ marginBottom: 16 }}>

          {/* ── Header row: board badge + region chips + tag picker ── */}
          <div className="feed-post-header">
            <div className="feed-post-board-row">
              <span className="feed-post-board-group" style={{ gap: 6, flexWrap: "wrap" }}>

                {/* Tag picker shell */}
                <div style={{ position: "relative" }} ref={tagShellRef}>
                  <div style={{ display: "flex", gap: 6, alignItems: "center", flexWrap: "wrap" }}>
                    {/* Board chip — click to open picker */}
                    <button
                      type="button"
                      onClick={() => { if (!isUserJailed) { setTagOpen(v => !v); setTagPickedContinent(null); } }}
                      style={{ background: "none", border: "none", padding: 0, cursor: isUserJailed ? "default" : "pointer" }}
                    >
                      <BoardBadge boardName={selectedBoard.name} />
                    </button>

                    {/* Country chip */}
                    {selectedCountry && (
                      <span style={{ display: "inline-flex", alignItems: "center", gap: 4 }}>
                        <GeoBadge country={selectedCountry} />
                        <button
                          type="button"
                          onClick={() => setSelectedCountry("")}
                          style={{ display: "inline-flex", alignItems: "center", justifyContent: "center", width: 16, height: 16, borderRadius: 999, border: "none", background: "#2d3748", color: "#94a3b8", fontSize: 12, lineHeight: 1, cursor: "pointer", padding: 0, flexShrink: 0 }}
                        >×</button>
                      </span>
                    )}

                    {/* + country button */}
                    {!selectedCountry && !isUserJailed && (
                      <button
                        type="button"
                        onClick={() => setTagOpen(v => !v)}
                        style={{ display: "inline-flex", alignItems: "center", gap: 3, padding: "2px 8px", borderRadius: 999, border: "1px dashed #3f4756", background: "none", color: "#64748b", fontSize: 11, fontWeight: 700, cursor: "pointer" }}
                      >+ country</button>
                    )}
                  </div>

                  {/* Tag dropdown — two scrollable columns side by side */}
                  {tagOpen && (
                    <div style={{
                      position: "absolute", top: "calc(100% + 6px)", left: 0,
                      background: "#1e2028", border: "1px solid #374151", borderRadius: 12,
                      boxShadow: "0 8px 32px rgba(0,0,0,0.5)", zIndex: 200,
                      display: "flex", flexDirection: "column", width: 340,
                    }}>
                      {/* Close button row */}
                      <div style={{ display: "flex", alignItems: "center", padding: "8px 10px 4px", borderBottom: "1px solid #2a2d38" }}>
                        <button
                          type="button"
                          onClick={() => setTagOpen(false)}
                          style={{ display: "flex", alignItems: "center", justifyContent: "center", width: 22, height: 22, borderRadius: 999, border: "none", background: "#2d2f3a", color: "#94a3b8", fontSize: 14, lineHeight: 1, cursor: "pointer", padding: 0, flexShrink: 0 }}
                        >×</button>
                        <span style={{ marginLeft: 8, fontSize: 11, fontWeight: 700, color: "#4b5563", textTransform: "uppercase", letterSpacing: "0.08em" }}>Select board &amp; country</span>
                      </div>

                      {/* Two columns */}
                      <div style={{ display: "flex", minHeight: 0 }}>
                        {/* Board column */}
                        {!isUserJailed && (
                          <div style={{ width: 130, flexShrink: 0, borderRight: "1px solid #2a2d38", overflowY: "auto", maxHeight: 260, paddingTop: 4, paddingBottom: 4 }}>
                            <div className="search-section-label">Board</div>
                            {BOARDS.filter(b => !b.virtual).map(b => (
                              <button
                                key={b.slug}
                                type="button"
                                onClick={() => { setSelectedBoardSlug(b.slug); }}
                                style={{
                                  display: "flex", alignItems: "center", gap: 7, width: "100%",
                                  padding: "6px 10px", border: "none", background: b.slug === selectedBoardSlug ? "#2d2f3a" : "none",
                                  color: b.slug === selectedBoardSlug ? "#c084fc" : "#e2e8f0",
                                  fontSize: 12, fontWeight: b.slug === selectedBoardSlug ? 700 : 500,
                                  cursor: "pointer", textAlign: "left",
                                }}
                              >
                                <span style={{ fontSize: 14, flexShrink: 0 }}>{b.icon}</span>
                                <span style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{b.name}</span>
                              </button>
                            ))}
                          </div>
                        )}

                        {/* Country column */}
                        <div style={{ flex: 1, overflowY: "auto", maxHeight: 260, paddingTop: 4, paddingBottom: 4 }}>
                          {tagPickedContinent ? (
                            <>
                              <div className="search-section-label" style={{ display: "flex", alignItems: "center", gap: 4 }}>
                                <button type="button" onClick={() => setTagPickedContinent(null)} style={{ background: "none", border: "none", color: "#c084fc", fontSize: 11, fontWeight: 700, cursor: "pointer", padding: 0 }}>← Back</button>
                                <span>{tagPickedContinent}</span>
                              </div>
                              {COUNTRIES_WITH_FLAGS.filter(c => COUNTRY_CONTINENT[c.name] === tagPickedContinent).map(c => (
                                <button
                                  key={c.name}
                                  type="button"
                                  onClick={() => { setSelectedCountry(c.name); setTagOpen(false); setTagPickedContinent(null); }}
                                  style={{
                                    display: "flex", alignItems: "center", gap: 7, width: "100%",
                                    padding: "6px 10px", border: "none",
                                    background: c.name === selectedCountry ? "#2d2f3a" : "none",
                                    color: c.name === selectedCountry ? "#c084fc" : "#e2e8f0",
                                    fontSize: 12, fontWeight: c.name === selectedCountry ? 700 : 500,
                                    cursor: "pointer", textAlign: "left",
                                  }}
                                >
                                  <span style={{ fontSize: 15, flexShrink: 0 }}>{c.flag}</span>
                                  <span style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{c.name}</span>
                                </button>
                              ))}
                            </>
                          ) : (
                            <>
                              <div className="search-section-label">Region</div>
                              {CONTINENTS.filter(c => c !== "World").map(c => (
                                <button
                                  key={c}
                                  type="button"
                                  onClick={() => setTagPickedContinent(c)}
                                  style={{
                                    display: "flex", alignItems: "center", gap: 7, width: "100%",
                                    padding: "6px 10px", border: "none", background: "none",
                                    color: "#e2e8f0", fontSize: 12, fontWeight: 500,
                                    cursor: "pointer", textAlign: "left",
                                  }}
                                >
                                  <span style={{ fontSize: 14, flexShrink: 0 }}>🌍</span>
                                  <span style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{c} →</span>
                                </button>
                              ))}
                            </>
                          )}
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                {isUserJailed && (
                  <span style={{ fontSize: 11, fontWeight: 700, color: "#fbbf24" }}>🪹 Caged</span>
                )}
              </span>

              <span className="feed-post-time">now</span>
            </div>
          </div>

          {/* ── Author row ── */}
          <div className="feed-post-main" style={{ paddingBottom: 0, borderBottom: "none" }}>
            <div className="feed-post-author-row">
              {(() => {
                const browserId = getBrowserId();
                const isMod = !!user && (userRole === "mod" || userRole === "admin");
                const isAdmin = userRole === "admin";
                const name = isMod ? getModName() : (previewName || `Anon #${shortId(browserId)}`);
                const color = getUserColor(browserId, previewName);
                const fakeRecord = { is_admin: isAdmin, is_mod: isMod && !isAdmin, username: name, browser_id: browserId };
                return <UserPill record={fakeRecord} name={name} color={color} />;
              })()}
            </div>

            {/* Title input */}
            <input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Give the thread a title…"
              disabled={isSending}
              style={{ width: "100%", boxSizing: "border-box", padding: 0, border: "none", fontSize: 20, fontWeight: 700, background: "transparent", color: "#f8fafc", outline: "none", marginTop: 10, marginBottom: 4, touchAction: "manipulation" }}
            />

            {/* Body textarea */}
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder={attachment ? "Add a caption (optional)…" : "What’s going on?"}
              disabled={isSending}
              rows={5}
              style={{ width: "100%", boxSizing: "border-box", padding: 0, border: "none", fontSize: 16, resize: "none", background: "transparent", color: "#d4dde7", outline: "none", minHeight: 90, fontFamily: "inherit", lineHeight: 1.6, touchAction: "manipulation" }}
            />
          </div>

          {/* Attachment preview */}
          {attachment && (
            <div style={{ marginTop: 10, position: "relative" }}>
              <PostAttachment attachment={attachment} />
              <button type="button" onClick={() => setAttachment(null)} style={{ position: "absolute", top: 6, right: 6, background: "rgba(0,0,0,0.6)", border: "none", color: "#fff", borderRadius: 999, width: 22, height: 22, cursor: "pointer", fontSize: 12, display: "flex", alignItems: "center", justifyContent: "center" }}>✕</button>
            </div>
          )}

          {/* Link input mode */}
          {attachMode === "link" && (
            <div style={{ display: "flex", gap: 8, marginTop: 10 }}>
              <input
                value={linkInput}
                onChange={(e) => setLinkInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleAddLink()}
                placeholder="Paste a URL..."
                autoFocus
                style={{ flex: 1, minWidth: 0, padding: "6px 12px", borderRadius: 8, border: "1px solid #3f4756", background: "#0f1117", color: "#f8fafc", fontSize: 16, outline: "none" }}
              />
              <button type="button" onClick={handleAddLink} disabled={linkLoading} style={{ flexShrink: 0, padding: "6px 12px", borderRadius: 8, border: "none", background: "#c084fc", color: "#14081d", fontWeight: 700, fontSize: 13, cursor: "pointer" }}>
                {linkLoading ? "…" : "Add"}
              </button>
            </div>
          )}

          {/* Hidden file inputs */}
          <input ref={imageInputRef} type="file" accept="image/*" style={{ display: "none" }} onChange={(e) => e.target.files[0] && handleFileUpload(e.target.files[0], "image")} />
          <input ref={videoInputRef} type="file" accept="video/*" style={{ display: "none" }} onChange={(e) => e.target.files[0] && handleFileUpload(e.target.files[0], "video")} />

          {/* ── Bottom actions (mirrors feed-post-actions style) ── */}
          <div className="feed-post-actions" style={{ marginTop: 14, borderTop: "1px solid #2e303a", paddingTop: 14 }}>
            {!attachment && attachMode !== "link" && (
              <>
                <button type="button" onClick={() => setAttachMode("link")} className="feed-post-action-pill">🔗 Link</button>
                <button type="button" onClick={() => imageInputRef.current?.click()} disabled={uploadLoading} className="feed-post-action-pill">{uploadLoading ? "…" : "🖼 Photo"}</button>
                <button type="button" onClick={() => videoInputRef.current?.click()} disabled={uploadLoading} className="feed-post-action-pill">{uploadLoading ? "…" : "🎥 Video"}</button>
              </>
            )}
            {attachMode === "link" && (
              <button type="button" onClick={() => { setAttachMode(null); setLinkInput(""); }} className="feed-post-action-pill">Cancel</button>
            )}
            <button
              onClick={createPost}
              disabled={isSending}
              className="feed-post-action-pill"
              style={{ marginLeft: "auto", background: isSending ? "#3b1f52" : "#c084fc", color: "#14081d", borderColor: "#c084fc", fontWeight: 700, opacity: isSending ? 0.7 : 1, cursor: isSending ? "default" : "pointer" }}
            >
              {isSending ? "Sending…" : "Post"}
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}

// ==============================
// POST PAGE (WITH MOD CONTROLS 🔥)
// ==============================
function PostPage({ user, userRole, memberUsername }) {
  const { id } = useParams();
  const [searchParams] = useSearchParams();
  const highlightId = searchParams.get("highlight");
  const navigate = useNavigate();

  const location = useLocation();
  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);
  const [text, setText] = useState("");
  const [isSendingComment, setIsSendingComment] = useState(false);
  const [pendingComments, setPendingComments] = useState([]);
  const [commentSort] = useState("oldest");
  const [scrollToBottom, setScrollToBottom] = useState(true);
  const [replyTarget, setReplyTarget] = useState(null);
  const [reactions, setReactions] = useState({});
  const [anonUsername, setAnonUsername] = useState(null);
  const [commentAttachment, setCommentAttachment] = useState(null);
  const [commentUploadLoading, setCommentUploadLoading] = useState(false);
  const commentMediaRef = useRef(null);
  const chatWindowRef = useRef(null);
  const isAtBottomRef = useRef(true);
  const highlightedRef = useRef(false);
  const scrolledToCommentsRef = useRef(false);
  // Capture intent once at mount — never re-read location so no re-renders can flip it
  const shouldScrollToCommentsRef = useRef(!!location.state?.scrollToComments);

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [id]);

  useEffect(() => {
    if (!shouldScrollToCommentsRef.current || scrolledToCommentsRef.current || comments.length === 0) return;
    scrolledToCommentsRef.current = true;
    const win = chatWindowRef.current;
    if (win) win.scrollTop = win.scrollHeight;
    setTimeout(() => window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" }), 50);
  }, [comments]);

  useEffect(() => {
    if (!highlightId || highlightedRef.current) return;
    const win = chatWindowRef.current;
    const el = win?.querySelector(`[data-comment-id="${highlightId}"]`);
    if (!el) return;
    highlightedRef.current = true;

    // Step 1: scroll the page down to the comments section
    const shell = document.querySelector(".comments-shell");
    if (shell) shell.scrollIntoView({ behavior: "smooth" });

    // Step 2: after page scroll settles, scroll chat window to the comment
    setTimeout(() => {
      const top = Math.max(0, el.offsetTop - win.clientHeight / 2 + el.offsetHeight / 2);
      win.scrollTo({ top, behavior: "smooth" });

      // Step 3: flash highlight after scroll lands
      setTimeout(() => {
        const bubble = el.querySelector(".chat-bubble");
        if (bubble) {
          bubble.classList.add("highlight");
          setTimeout(() => bubble.classList.remove("highlight"), 2500);
        }
      }, 400);
    }, 450);
  }, [comments, highlightId]);

  useEffect(() => {
    if (user) { setAnonUsername(null); return; }
    (async () => {
      const authHeaders = getOptionalAuthHeader();
      try {
        const res = await fetch("https://daboysforumip.coldbrainarchive.workers.dev/my-username", { headers: authHeaders });
        if (res.ok) { const d = await res.json(); setAnonUsername(d.username || null); }
      } catch {}
    })();
  }, [user]);

  async function handleReact(commentId, emoji) {
    const myId = getBrowserId();
    const hasReacted = (reactions[commentId]?.[emoji] || []).includes(myId);
    // Optimistic update
    setReactions((prev) => {
      const commentReactions = { ...(prev[commentId] || {}) };
      const voters = commentReactions[emoji] ? [...commentReactions[emoji]] : [];
      if (hasReacted) {
        const updated = voters.filter((v) => v !== myId);
        if (updated.length === 0) delete commentReactions[emoji];
        else commentReactions[emoji] = updated;
      } else {
        commentReactions[emoji] = [...voters, myId];
      }
      return { ...prev, [commentId]: commentReactions };
    });
    // Persist
    const reactUsername = memberUsername || anonUsername || getStoredUser()?.username || null;
    fetch(`${WORKER_URL}/react-comment`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...getOptionalAuthHeader() },
      body: JSON.stringify({ comment_id: commentId, browser_id: myId, emoji, action: hasReacted ? "remove" : "add", username: reactUsername })
    }).catch(() => {});
  }
  const [voteData, setVoteData] = useState({ score: 0, myVote: 0 });
  const [shareLabel, setShareLabel] = useState("Share");

  const isMod = !!user && (userRole === "mod" || userRole === "admin");
  const isMember = !!user && !isMod;
  const [isCaged, setIsCaged] = useState(false);

  useEffect(() => {
    if (isMod) return;
    const browserId = getBrowserId();
    fetch(`${WORKER_URL}/check-jailed?browser_id=${browserId}`)
      .then(r => r.json()).then(d => { if (d.jailed) setIsCaged(true); }).catch(() => {});
  }, [isMod]);

  const load = useCallback(async () => {
    const res = await fetch(`${WORKER_URL}/get-post?id=${id}`);
    if (!res.ok) return;
    const { post: p, comments: c } = await res.json();

    setPost(hydratePostWithBoardTag(p));
    const all = c || [];
    const validIds = new Set();
    // Two passes: first collect top-level, then replies whose parent is valid
    all.filter((comment) => !comment.parent_comment_id).forEach((comment) => validIds.add(comment.id));
    let changed = true;
    while (changed) {
      changed = false;
      all.forEach((comment) => {
        if (!validIds.has(comment.id) && comment.parent_comment_id && validIds.has(comment.parent_comment_id)) {
          validIds.add(comment.id);
          changed = true;
        }
      });
    }
    const filtered = all.filter((comment) => validIds.has(comment.id));
    setComments(filtered);
    setPendingComments([]);
    const commentIds = filtered.map((c) => c.id);
    const [votes, reactionData] = await Promise.all([
      p?.id ? fetchVotesForPosts([p.id]) : Promise.resolve({}),
      fetchReactions(commentIds)
    ]);
    if (p?.id) setVoteData(votes[p.id] || { score: 0, myVote: 0 });
    setReactions(reactionData);
  }, [id]);

  useEffect(() => {
    const timeoutId = window.setTimeout(() => {
      void load();
    }, 0);
    const i = window.setInterval(() => {
      void load();
    }, 2000);
    return () => {
      window.clearTimeout(timeoutId);
      window.clearInterval(i);
    };
  }, [load]);

  useEffect(() => {
    const el = chatWindowRef.current;
    if (!el) return;
    if (isAtBottomRef.current) {
      el.scrollTop = el.scrollHeight;
    }
  }, [comments.length, pendingComments.length]);

  async function handleCommentFileUpload(file) {
    const type = file.type.startsWith("image/") ? "image" : "video";
    setCommentUploadLoading(true);
    try {
      const formData = new FormData();
      formData.append("file", file);
      const res = await fetch(`${WORKER_URL}/upload`, { method: "POST", body: formData });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Upload failed");
      setCommentAttachment({ type, url: data.url });
    } catch (err) {
      alert("Upload failed: " + err.message);
    } finally {
      setCommentUploadLoading(false);
    }
  }

  const submitComment = async (content, parentCommentId = null, attachment = null) => {
    if (!content.trim() && !attachment || post?.locked) return;
    if (isSendingComment) return;
    if (isCaged && getBoardNameFromPost(post) !== "Cage") {
      alert("🪹 You are caged — you can only post in the Cage board");
      return;
    }

    const pendingId = crypto.randomUUID();
    const finalContent = attachment ? content + ATTACH_MARKER + JSON.stringify(attachment) + "]" : content;

    try {
      const browserId = getBrowserId();
      const modMetadata = buildModMetadata(getStoredUser(), memberUsername);
      const authHeaders = getOptionalAuthHeader();
      setIsSendingComment(true);
      setPendingComments((current) => [
        ...current,
        {
          id: pendingId,
          content: finalContent,
          created_at: new Date().toISOString(),
          browser_id: browserId,
          parent_comment_id: parentCommentId,
          username: modMetadata.username,
          is_mod: modMetadata.is_mod,
          isPending: true
        }
      ]);

      const res = await fetch(
        "https://daboysforumip.coldbrainarchive.workers.dev/add-comment",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            ...authHeaders
          },
          body: JSON.stringify({
            content: finalContent,
            post_id: id,
            parent_comment_id: parentCommentId,
            browser_id: browserId,
            ...modMetadata
          })
        }
      );

      const result = await res.json();
      if (!res.ok) {
        setPendingComments((current) => current.filter((comment) => comment.id !== pendingId));
        setIsSendingComment(false);
        if (result.error === "Banned") {
          alert("🚫 You are banned from commenting");
        } else {
          alert(result.error);
        }
        throw new Error(result.error);
      }

      if (user && memberUsername) {
        fetch(`${WORKER_URL}/backfill-username`, {
          method: "POST",
          headers: { "Content-Type": "application/json", ...getOptionalAuthHeader() },
          body: JSON.stringify({ browser_id: browserId, username: memberUsername })
        }).catch(() => {});
      }

      setIsSendingComment(false);
      await load();
    } catch (err) {
      setPendingComments((current) => current.filter((comment) => comment.id !== pendingId));
      setIsSendingComment(false);
      console.error(err);
    }
  };

  if (!post) return <div>Loading...</div>;

  const activeBoard = getBoardNameFromPost(post);
  const postIsMod = isModPost(post);
  const postAuthorLabel = post.username || `Anon #${shortId(post.browser_id)}`;
  const allComments = [...comments, ...pendingComments];
  const flatComments = [...allComments].sort((a, b) => {
    if (a.pinned && !b.pinned) return -1;
    if (!a.pinned && b.pinned) return 1;
    const tA = new Date(a.created_at).getTime();
    const tB = new Date(b.created_at).getTime();
    return commentSort === "oldest" ? tA - tB : tB - tA;
  });
  const topLevelComments = flatComments.filter((c) => !c.parent_comment_id);
  function getThreadReplies(rootId) {
    const result = [];
    const queue = [rootId];
    while (queue.length > 0) {
      const parentId = queue.shift();
      const direct = allComments.filter((c) => c.parent_comment_id === parentId);
      result.push(...direct);
      direct.forEach((r) => queue.push(r.id));
    }
    return result.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
  }

  return (
    <div className="home-shell">
      <SearchBar />

      <main className="home-feed" style={{ textAlign: "left" }}>
        <div className="content-card feed-post-card" style={{ marginBottom: 16 }}>
          <div className="feed-post-header">
            <div className="feed-post-board-row">
              <span className="feed-post-board-group">
                <button
                  type="button"
                  onClick={() => navigate(-1)}
                  style={{
                    display: "inline-flex",
                    alignItems: "center",
                    justifyContent: "center",
                    width: 26,
                    height: 26,
                    borderRadius: 999,
                    border: "none",
                    background: "#20262f",
                    color: "#dbe4ee",
                    fontSize: 12,
                    fontWeight: 800,
                    cursor: "pointer",
                    flexShrink: 0
                  }}
                >
                  ←
                </button>
                {activeBoard && (() => {
                  const boardSlug = BOARDS.find((b) => b.name === activeBoard)?.slug;
                  return boardSlug ? (
                    <Link to={`/board/${boardSlug}`} style={{ textDecoration: "none" }}>
                      <BoardBadge boardName={activeBoard} />
                    </Link>
                  ) : (
                    <BoardBadge boardName={activeBoard} />
                  );
                })()}
                {(post.pinned || post.locked) && (
                  <span className="feed-post-statuses">
                    {post.pinned && (
                      <span className="feed-post-status" style={{ color: "#f8fafc" }}>
                        📌
                      </span>
                    )}
                    {post.locked && (
                      <span className="feed-post-status" style={{ color: "#f87171" }}>
                        🔒
                      </span>
                    )}
                  </span>
                )}
              </span>
            </div>
          </div>

          {(() => { const { text: postPageText, attachment: postPageAttachment } = parsePostContent(post.content); return (
            <div style={{ padding: "14px 0 10px", borderTop: "1px solid rgba(148,163,184,0.12)" }}>
              <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap", marginBottom: 10 }}>
                <UserPill record={post} name={postAuthorLabel} color={getUserColor(post.browser_id, post.username)} />
                <span style={{ color: "#8fa0b6", fontWeight: 500, fontSize: 12 }}>Posted {timeAgo(post.created_at)}</span>
              </div>

              {(post.title || postPageText) && (
                <div style={{ border: "1px solid rgba(148,163,184,0.15)", borderRadius: 12, background: "#1a1d27", padding: "14px 16px", marginBottom: postPageAttachment ? 10 : 0 }}>
                  {post.title && (
                    <h2 style={{ margin: "0 0 8px", fontSize: 20, fontWeight: 800, color: "#f8fafc", lineHeight: 1.3, textAlign: "left" }}>
                      {post.title}
                    </h2>
                  )}
                  {postPageText && (
                    <p style={{ margin: 0, color: "#d4dde7", fontSize: 15, lineHeight: 1.55, whiteSpace: "pre-wrap", overflowWrap: "anywhere", textAlign: "left" }}>
                      {postPageText}
                    </p>
                  )}
                </div>
              )}
              {postPageAttachment && <div style={{ marginTop: 12 }}><PostAttachment attachment={postPageAttachment} /></div>}
            </div>
          ); })()}
          {!parsePostContent(post.content).attachment && <div style={{ height: 4 }} />}

          <div className="feed-post-actions">
            <button
              type="button"
              className="feed-post-action-pill"
              style={voteData.myVote === 1 ? { borderColor: "#c084fc", background: "rgba(192,132,252,0.15)" } : {}}
              onClick={async (event) => {
                event.preventDefault();
                const result = await voteOnPost(post.id, voteData.myVote === 1 ? 0 : 1);
                if (result.success) setVoteData({ score: result.score, myVote: result.myVote });
              }}
            >
              <span>👍</span>
              <span>{voteData.score}</span>
            </button>

            <button
              type="button"
              className="feed-post-action-pill"
              onClick={() => {
                const shell = document.querySelector(".comments-shell");
                if (shell) shell.scrollIntoView({ behavior: "smooth" });
                setTimeout(() => {
                  const el = chatWindowRef.current;
                  if (el) el.scrollTop = el.scrollHeight;
                }, 350);
              }}
            >
              <span>💬</span><span>{comments.length}</span>
            </button>

            <button
              type="button"
              className="feed-post-action-pill"
              onClick={async (event) => {
                event.preventDefault();
                const shareUrl = `${window.location.origin}/post/${post.id}`;
                try {
                  if (navigator.share) {
                    await navigator.share({ title: post.title, text: post.title, url: shareUrl });
                    setShareLabel("Shared");
                  } else if (navigator.clipboard?.writeText) {
                    await navigator.clipboard.writeText(shareUrl);
                    setShareLabel("Copied");
                  } else {
                    setShareLabel("Link ready");
                  }
                } catch (error) {
                  if (error?.name !== "AbortError") setShareLabel("Share failed");
                  return;
                }
                window.setTimeout(() => setShareLabel("Share"), 1800);
              }}
            >
              <span>↗</span>
              <span>{shareLabel}</span>
            </button>

            {isMember && memberUsername && post.username === memberUsername && (
              <button
                type="button"
                className="feed-post-action-pill"
                onClick={async () => {
                  if (!confirm("Delete your post?")) return;
                  await fetch(`${WORKER_URL}/delete-my-post`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json", ...getOptionalAuthHeader() },
                    body: JSON.stringify({ post_id: post.id, browser_id: getBrowserId() })
                  });
                  navigate(-1);
                }}
              >
                <span>🗑</span>
                <span>Delete</span>
              </button>
            )}

            {isMod && (
              <button
                type="button"
                className="feed-post-action-pill"
                onClick={() => { if (!confirm("Delete this post?")) return; modAction({ type: "delete_post", post_id: post.id }); }}
              >
                <span>🗑</span>
                <span>Delete</span>
              </button>
            )}
          </div>

          {/* 🔥 MOD CONTROLS (PIN / LOCK) */}
          {isMod && (
            <div style={{ marginTop: 14, marginBottom: 10 }}>

              {post.pinned ? (
                <button
                  onClick={async () => {
                    await modAction({ type: "pin_post", post_id: post.id, pinned: false, pinned_global: false });
                    load();
                  }}
                >
                  📌 Unpin
                </button>
              ) : (
                <>
                  <button
                    onClick={async () => {
                      await modAction({ type: "pin_post", post_id: post.id, pinned: true, pinned_global: false });
                      load();
                    }}
                  >
                    📌 Pin to Board
                  </button>
                  <button
                    onClick={async () => {
                      await modAction({ type: "pin_post", post_id: post.id, pinned: true, pinned_global: true });
                      load();
                    }}
                  >
                    📌 Pin to Forum
                  </button>
                </>
              )}

              <button
                onClick={async () => {
                  await modAction({ type: "lock_post", post_id: post.id, locked: !post.locked });
                  load();
                }}
              >
                {post.locked ? "Unlock" : "🔒 Lock"}
              </button>
            </div>
          )}
        </div>

        <section className="comments-shell">
          <div className="content-card comments-panel" style={{ padding: 0, overflow: "clip", display: "flex", flexDirection: "column", height: "min(600px, 80dvh)" }}>
            <div className="chat-panel-header" style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
              <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <button
                  type="button"
                  onClick={() => navigate(-1)}
                  style={{
                    display: "inline-flex",
                    alignItems: "center",
                    justifyContent: "center",
                    width: 26,
                    height: 26,
                    borderRadius: 999,
                    border: "none",
                    background: "#20262f",
                    color: "#dbe4ee",
                    fontSize: 12,
                    fontWeight: 800,
                    cursor: "pointer",
                    flexShrink: 0
                  }}
                >
                  ←
                </button>
                <span className="comments-panel-title">{comments.length} Chats</span>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                <button
                  type="button"
                  onClick={() => { window.scrollTo({ top: 0, behavior: "smooth" }); document.documentElement.scrollTo({ top: 0, behavior: "smooth" }); }}
                  style={{ display: "inline-flex", alignItems: "center", justifyContent: "center", width: 26, height: 26, borderRadius: 999, border: "none", background: "#20262f", color: "#dbe4ee", fontSize: 12, fontWeight: 800, cursor: "pointer", flexShrink: 0 }}
                >
                  ↑
                </button>
                <button
                  type="button"
                  onClick={() => { window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" }); document.documentElement.scrollTo({ top: document.documentElement.scrollHeight, behavior: "smooth" }); }}
                  style={{ display: "inline-flex", alignItems: "center", justifyContent: "center", width: 26, height: 26, borderRadius: 999, border: "none", background: "#20262f", color: "#dbe4ee", fontSize: 12, fontWeight: 800, cursor: "pointer", flexShrink: 0 }}
                >
                  ↓
                </button>
                <button
                  type="button"
                  className="feed-post-action-pill"
                  onClick={() => {
                    const el = chatWindowRef.current;
                    if (el) el.scrollTo({ top: scrollToBottom ? el.scrollHeight : 0, behavior: "smooth" });
                    setScrollToBottom(v => !v);
                  }}
                >
                  {scrollToBottom ? "Newest" : "Oldest"}
                </button>
              </div>
            </div>

            <div
              className="chat-window"
              ref={chatWindowRef}
              onScroll={() => {
                const el = chatWindowRef.current;
                if (!el) return;
                isAtBottomRef.current = el.scrollHeight - el.scrollTop - el.clientHeight < 60;
              }}
            >
              {flatComments.map((c) => (
                <ChatMessage
                  key={c.id}
                  comment={c}
                  postBrowserId={post.browser_id}
                  postUsername={post.username || null}
                  canDelete={isMod || (isMember && memberUsername && c.username === memberUsername)}
                  onDelete={async () => {
                    if (isMod) {
                      await modAction({ type: "delete_comment", comment_id: c.id });
                    } else {
                      await fetch(`${WORKER_URL}/delete-my-comment`, {
                        method: "POST",
                        headers: { "Content-Type": "application/json", ...getOptionalAuthHeader() },
                        body: JSON.stringify({ comment_id: c.id, browser_id: getBrowserId() })
                      });
                    }
                    await load();
                  }}
                  canPin={isMod}
                  onPin={async () => {
                    await modAction({ type: "pin_comment", comment_id: c.id, pinned: !c.pinned });
                    await load();
                  }}
                  onReply={(msg) => setReplyTarget(msg)}
                  onReact={handleReact}
                  reactions={reactions}
                  allComments={allComments}
                  onFindParent={(parentId) => {
                    const win = chatWindowRef.current;
                    const el = win?.querySelector(`[data-comment-id="${parentId}"]`);
                    if (win && el) {
                      const target = el.offsetTop - (win.clientHeight / 2) + (el.offsetHeight / 2);
                      win.scrollTo({ top: target, behavior: "smooth" });
                      const bubble = el.querySelector(".chat-bubble");
                      if (bubble) {
                        setTimeout(() => {
                          bubble.classList.add("highlight");
                          setTimeout(() => bubble.classList.remove("highlight"), 1000);
                        }, 500);
                      }
                    }
                  }}
                />
              ))}
            </div>

            {!post.locked && (
              <div className="chat-compose">
                <input
                  ref={commentMediaRef}
                  type="file"
                  accept="image/*,video/*"
                  style={{ display: "none" }}
                  onChange={(e) => {
                    const file = e.target.files[0];
                    if (file) handleCommentFileUpload(file);
                    e.target.value = "";
                  }}
                />
                {replyTarget && (
                  <div className="chat-reply-preview">
                    <div className="chat-reply-preview-inner">
                      <span className="chat-reply-preview-name">
                        {replyTarget.username || `Anon #${shortId(replyTarget.browser_id)}`}
                      </span>
                      <p className="chat-reply-preview-text">{parsePostContent(replyTarget.content).text}</p>
                    </div>
                    <button
                      type="button"
                      className="chat-reply-dismiss"
                      onClick={() => setReplyTarget(null)}
                    >
                      ✕
                    </button>
                  </div>
                )}
                {commentAttachment && (
                  <div style={{ padding: "6px 12px 0", display: "flex", alignItems: "flex-start", gap: 8 }}>
                    <div style={{ position: "relative", display: "inline-flex" }}>
                      {commentAttachment.type === "image"
                        ? <img src={commentAttachment.url} alt="" style={{ maxHeight: 72, maxWidth: 128, borderRadius: 8, objectFit: "cover" }} />
                        : <video src={commentAttachment.url} style={{ maxHeight: 72, maxWidth: 128, borderRadius: 8 }} muted />
                      }
                      <button
                        type="button"
                        onClick={() => setCommentAttachment(null)}
                        style={{ position: "absolute", top: 2, right: 2, background: "rgba(0,0,0,0.65)", border: "none", color: "#fff", borderRadius: 999, width: 18, height: 18, cursor: "pointer", fontSize: 10, display: "flex", alignItems: "center", justifyContent: "center", padding: 0 }}
                      >✕</button>
                    </div>
                  </div>
                )}
                <div className="chat-input-row">
                  <button
                    type="button"
                    onClick={() => commentMediaRef.current?.click()}
                    disabled={commentUploadLoading || isSendingComment}
                    style={{ flexShrink: 0, background: "none", border: "none", color: commentAttachment ? "#c084fc" : "#8fa0b6", fontSize: 18, cursor: "pointer", padding: "0 4px", lineHeight: 1, display: "flex", alignItems: "center" }}
                    title="Attach photo or video"
                  >
                    {commentUploadLoading ? <span style={{ fontSize: 12 }}>…</span> : "📎"}
                  </button>
                  <div className="chat-input-bubble">
                    <textarea
                      className="chat-input"
                      value={text}
                      onChange={(e) => setText(e.target.value)}
                      placeholder={commentAttachment ? "Add a caption (optional)…" : "Message..."}
                      disabled={isSendingComment}
                      rows={1}
                      onKeyDown={(e) => {
                        if (e.key === "Enter" && !e.shiftKey) {
                          e.preventDefault();
                          if (!text.trim() && !commentAttachment) return;
                          const content = text;
                          const attachment = commentAttachment;
                          const parentId = replyTarget?.id || null;
                          setText("");
                          setReplyTarget(null);
                          setCommentAttachment(null);
                          isAtBottomRef.current = true;
                          submitComment(content, parentId, attachment);
                        }
                      }}
                    />
                  </div>
                  <button
                    type="button"
                    className="chat-send-btn"
                    disabled={isSendingComment || (!text.trim() && !commentAttachment)}
                    onClick={() => {
                      if (!text.trim() && !commentAttachment) return;
                      const content = text;
                      const attachment = commentAttachment;
                      const parentId = replyTarget?.id || null;
                      setText("");
                      setReplyTarget(null);
                      setCommentAttachment(null);
                      isAtBottomRef.current = true;
                      submitComment(content, parentId, attachment);
                    }}
                  >
                    ↑
                  </button>
                </div>
              </div>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}
// ==============================
// MOD PANEL (FINAL)
// ==============================
function ModPanel() {
  const isAdmin = localStorage.getItem("user_role") === "admin";
  const [users, setUsers] = useState([]);
  const [bots, setBots] = useState([]);
  const [bans, setBans] = useState([]);
  const [jailed, setJailed] = useState([]);
  const [members, setMembers] = useState([]);
  const [archivedPosts, setArchivedPosts] = useState([]);
  const [archiveExpanded, setArchiveExpanded] = useState(false);
  const [archiveSearch, setArchiveSearch] = useState("");
  const [botConfig, setBotConfig] = useState(null);
  const [savingBotConfig, setSavingBotConfig] = useState(false);
  const [botLogs, setBotLogs] = useState([]);
  const [botLogsLoading, setBotLogsLoading] = useState(false);
  const [botTriggering, setBotTriggering] = useState(false);
  const [expandedLog, setExpandedLog] = useState(null);
  const [botPanelOpen, setBotPanelOpen] = useState(true);
  const [botLogsOpen, setBotLogsOpen] = useState(true);
  const [botFeedsOpen, setBotFeedsOpen] = useState(false);
  const feedDragIndex = useRef(null);
  const [feedGroupExpanded, setFeedGroupExpanded] = useState({});
  const [browserIdByUsername, setBrowserIdByUsername] = useState({});
  const [memberSearch, setMemberSearch] = useState("");
  const [memberSortBy, setMemberSortBy] = useState("joined_desc");
  const [email, setEmail] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [search, setSearch] = useState("");
  const [sortBy, setSortBy] = useState("joined_desc");
  // LOAD DATA
  const load = useCallback(async () => {
    const authHeaders = getAuthHeader();
    const [modDataRes, membersRes, botConfigRes, botLogsRes] = await Promise.all([
      fetch(`${WORKER_URL}/get-mod-data`, { headers: authHeaders }),
      fetch(`${WORKER_URL}/get-members`, { headers: authHeaders }),
      fetch(`${WORKER_URL}/bot-config`, { headers: authHeaders }),
      fetch(`${WORKER_URL}/bot-logs`, { headers: authHeaders }),
    ]);

    const modData = modDataRes.ok ? await modDataRes.json() : {};
    const membersJson = membersRes.ok ? await membersRes.json() : { members: [] };
    const botConfigJson = botConfigRes.ok ? await botConfigRes.json() : {};
    const botLogsJson = botLogsRes.ok ? await botLogsRes.json() : {};

    const posts = modData.posts || [];
    const comments = modData.comments || [];
    const bans = modData.bans || [];
    const jailedData = modData.jailed || [];

    setBans(bans);
    setJailed(jailedData);
    setMembers(membersJson.members || []);
    setEmail(getStoredUser()?.username || "");
    setBotConfig(botConfigJson.config || null);
    setBotLogs(botLogsJson.logs || []);
    setArchivedPosts(modData.deletedPosts || []);

    const all = [...posts, ...comments];
    const map = {};
    const ipByUsername = {};
    const browserIdByUsername = {};

    all.forEach((u) => {
      if (u.username && u.ip_hash) ipByUsername[u.username] = u.ip_hash;
      if (u.username && u.browser_id) browserIdByUsername[u.username] = u.browser_id;
      if (!u.browser_id || !u.username) return;

      const existing = map[u.browser_id];
      const entryDate = u.created_at ? new Date(u.created_at) : null;
      const earliestDate = existing?.joined_at
        ? (entryDate && entryDate < existing.joined_at ? entryDate : existing.joined_at)
        : entryDate;

      map[u.browser_id] = {
        browser_id: u.browser_id,
        username: u.username,
        ip_hash: u.ip_hash,
        joined_at: earliestDate
      };
    });

    const memberUsernames = new Set((membersJson.members || []).map(m => m.username).filter(Boolean));
    const allAnon = Object.values(map).filter(u => !memberUsernames.has(u.username));
    setBots(allAnon.filter(u => BOT_USERNAMES.includes(u.username)));
    setUsers(allAnon.filter(u => !BOT_USERNAMES.includes(u.username)));
    setBrowserIdByUsername(browserIdByUsername);
  }, []);

  useEffect(() => {
    const timeoutId = window.setTimeout(() => {
      void load();
    }, 0);
    return () => window.clearTimeout(timeoutId);
  }, [load]);

  // LOGOUT
  const logout = () => {
    localStorage.removeItem("auth_token");
    localStorage.removeItem("auth_user");
    localStorage.removeItem("user_role");
    window.location.reload();
  };

  // UPDATE PASSWORD
  const updatePassword = async () => {
    if (!newPassword) return;
    try {
      const res = await fetch(`${WORKER_URL}/update-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...getAuthHeader() },
        body: JSON.stringify({ newPassword })
      });
      const data = await res.json();
      if (!res.ok) return alert(data.error || "Failed to update password");
      alert("Password updated 🔑");
      setNewPassword("");
    } catch (err) { alert(err.message); }
  };

  // BAN SYSTEM
  const isBanned = (u) =>
    bans.some(
      (b) =>
        b.browser_id === u.browser_id ||
        b.ip_hash === u.ip_hash ||
        b.username === u.username
    );

  const toggleBan = async (u) => {
    if (isBanned(u)) {
      await modAction({ type: "unban", browser_id: u.browser_id });
    } else {
      await modAction({ type: "ban", browser_id: u.browser_id, username: u.username, ip_hash: u.ip_hash });
    }
    load();
  };

  // JAIL SYSTEM
  const isJailed = (u) => jailed.some((j) => j.browser_id === u.browser_id);

  const toggleJail = async (u) => {
    if (isJailed(u)) {
      await modAction({ type: "unjail", browser_id: u.browser_id });
    } else {
      await modAction({ type: "jail", browser_id: u.browser_id, username: u.username, ip_hash: u.ip_hash });
    }
    load();
  };

  // DELETE USERNAME (gives them a fresh name next post)
  const deleteUsername = async (u) => {
    if (!confirm(`Clear "${u.username}"'s name? They'll get a new one next time they post.`)) return;
    await modAction({ type: "clear_username", browser_id: u.browser_id });
    load();
  };

  const triggerBot = async () => {
    setBotTriggering(true);
    const headers = getAuthHeader();
    await fetch("https://daboysforumip.coldbrainarchive.workers.dev/bot-trigger", { method: "POST", headers });
    // Refresh logs after a short delay to let the run start
    setTimeout(async () => {
      setBotLogsLoading(true);
      const h = getAuthHeader();
      const res = await fetch("https://daboysforumip.coldbrainarchive.workers.dev/bot-logs", { headers: h });
      const json = res.ok ? await res.json() : {};
      setBotLogs(json.logs || []);
      setBotLogsLoading(false);
      setBotTriggering(false);
    }, 3000);
  };

  const refreshLogs = async () => {
    setBotLogsLoading(true);
    const headers = getAuthHeader();
    const res = await fetch("https://daboysforumip.coldbrainarchive.workers.dev/bot-logs", { headers });
    const json = res.ok ? await res.json() : {};
    setBotLogs(json.logs || []);
    setBotLogsLoading(false);
  };

  const deleteLog = async (id) => {
    const headers = getAuthHeader();
    await fetch("https://daboysforumip.coldbrainarchive.workers.dev/bot-log-delete", {
      method: "POST",
      headers: { "Content-Type": "application/json", ...headers },
      body: JSON.stringify({ id }),
    });
    setBotLogs(prev => prev.filter(l => l.id !== id));
  };

  const saveBotConfig = async () => {
    setSavingBotConfig(true);
    const headers = getAuthHeader();
    await fetch("https://daboysforumip.coldbrainarchive.workers.dev/bot-config", {
      method: "POST",
      headers: { "Content-Type": "application/json", ...headers },
      body: JSON.stringify({ config: botConfig })
    });
    setSavingBotConfig(false);
  };

  const filteredUsers = search.trim()
    ? users.filter((u) => u.username.toLowerCase().includes(search.toLowerCase()))
    : users;

  const sortedUsers = [...filteredUsers].sort((a, b) => {
    if (sortBy === "joined_desc") return (b.joined_at || 0) - (a.joined_at || 0);
    if (sortBy === "joined_asc") return (a.joined_at || 0) - (b.joined_at || 0);
    if (sortBy === "name") return a.username.localeCompare(b.username);
    if (sortBy === "banned") {
      const aBanned = isBanned(a) ? 1 : 0;
      const bBanned = isBanned(b) ? 1 : 0;
      return bBanned - aBanned;
    }
    return 0;
  });

  return (
    <div style={{ width: "min(1280px, 100%)", margin: "0 auto", padding: "24px 20px 40px", boxSizing: "border-box", textAlign: "left" }}>
      <div style={{ marginBottom: 24 }}>
        <h2 style={{ margin: "0 0 4px", color: "#f8fafc", fontSize: 28, fontWeight: 800, letterSpacing: "-0.02em" }}>Profile</h2>
        <p style={{ color: "#94a3b8", fontSize: 14 }}>{email}</p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: 16, marginBottom: 24 }}>
        {/* Account */}
        <div className="content-card" style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          <h3 style={{ margin: 0, color: "#f8fafc", fontSize: 16, fontWeight: 700 }}>Account</h3>

          <button
            onClick={logout}
            style={{ padding: "10px 16px", borderRadius: 12, border: "1px solid #374151", background: "#1f2937", color: "#f8fafc", fontWeight: 700, cursor: "pointer", fontSize: 14 }}
          >
            🚪 Logout
          </button>

          <div style={{ display: "grid", gap: 8 }}>
            <input
              type="password"
              placeholder="New password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              style={{ width: "100%", boxSizing: "border-box", padding: "11px 14px", borderRadius: 10, border: "1px solid #3f4756", fontSize: 16, background: "#0f1117", color: "#f8fafc" }}
            />
            <button
              onClick={updatePassword}
              style={{ width: "100%", padding: "10px 16px", borderRadius: 12, border: "none", background: "#c084fc", color: "#14081d", fontWeight: 700, cursor: "pointer", fontSize: 14 }}
            >
              Update Password
            </button>
          </div>
        </div>

      </div>

      {/* Users */}
      <div className="content-card" style={{ padding: 0, overflow: "hidden" }}>
        <div style={{ padding: "14px 20px", borderBottom: "1px solid #2e303a", display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
          <h3 style={{ margin: 0, color: "#f8fafc", fontSize: 16, fontWeight: 700, marginRight: "auto" }}>
            Anonymous <span style={{ color: "#64748b", fontWeight: 500, fontSize: 13 }}>{sortedUsers.length}</span>
          </h3>
          <input
            placeholder="Search users…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{ padding: "7px 12px", borderRadius: 10, border: "1px solid #3f4756", background: "#0f1117", color: "#f8fafc", fontSize: 16, width: 180 }}
          />
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            style={{ padding: "7px 12px", borderRadius: 10, border: "1px solid #374151", background: "#1f2937", color: "#dbe4ee", fontSize: 13, cursor: "pointer" }}
          >
            <option value="joined_desc">Newest first</option>
            <option value="joined_asc">Oldest first</option>
            <option value="name">Name A–Z</option>
            <option value="banned">Banned first</option>
          </select>
        </div>
        <div style={{ display: "flex", flexDirection: "column" }}>
          {sortedUsers.map((u, i) => {
            const banned = isBanned(u);
            const jailedUser = isJailed(u);
            const rowBg = banned
              ? "rgba(248, 113, 113, 0.04)"
              : jailedUser
              ? "rgba(251, 191, 36, 0.04)"
              : "transparent";
            return (
              <div
                key={u.browser_id}
                style={{
                  padding: "12px 16px",
                  borderBottom: i < sortedUsers.length - 1 ? "1px solid #2e303a" : "none",
                  background: rowBg
                }}
              >
                {/* Info row */}
                <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 10 }}>
                  <div style={{ width: 32, height: 32, borderRadius: "50%", background: getUserColor(u.browser_id, u.username), display: "flex", alignItems: "center", justifyContent: "center", fontSize: 13, fontWeight: 800, color: "#0f1117", flexShrink: 0 }}>
                    {u.username[0].toUpperCase()}
                  </div>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 6, flexWrap: "wrap" }}>
                      <UserPill record={{ username: u.username, browser_id: u.browser_id }} name={u.username} color={getUserColor(u.browser_id, u.username)} />
                      {banned && <span style={{ fontSize: 10, fontWeight: 700, color: "#f87171", background: "rgba(248,113,113,0.12)", padding: "1px 6px", borderRadius: 999 }}>BANNED</span>}
                      {jailedUser && !banned && <span style={{ fontSize: 10, fontWeight: 700, color: "#fbbf24", background: "rgba(251,191,36,0.12)", padding: "1px 6px", borderRadius: 999 }}>CAGED</span>}
                    </div>
                    <div style={{ color: "#64748b", fontSize: 11, marginTop: 1 }}>
                      {u.joined_at ? `joined ${timeAgo(u.joined_at)} · ` : ""}{u.browser_id}
                    </div>
                  </div>
                </div>
                {/* Action row */}
                <div style={{ display: "flex", gap: 6 }}>
                  <button onClick={() => toggleJail(u)} style={{ flex: 1, padding: "7px 4px", borderRadius: 10, border: "none", background: jailedUser ? "#78350f" : "#451a03", color: jailedUser ? "#fde68a" : "#fbbf24", fontWeight: 700, cursor: "pointer", fontSize: 12 }}>
                    {jailedUser ? "Uncage" : "🪹 Cage"}
                  </button>
                  <button onClick={() => toggleBan(u)} style={{ flex: 1, padding: "7px 4px", borderRadius: 10, border: "none", background: banned ? "#1f2937" : "#7f1d1d", color: banned ? "#f8fafc" : "#fca5a5", fontWeight: 700, cursor: "pointer", fontSize: 12 }}>
                    {banned ? "Unban" : "Ban"}
                  </button>
                  <button onClick={() => deleteUsername(u)} title="Clear name" style={{ flex: 1, padding: "7px 4px", borderRadius: 10, border: "1px solid #374151", background: "#1f2937", color: "#94a3b8", fontWeight: 700, cursor: "pointer", fontSize: 12 }}>
                    🗑 Clear
                  </button>
                </div>
              </div>
            );
          })}
          {sortedUsers.length === 0 && (
            <div style={{ padding: "32px 20px", color: "#64748b", fontSize: 14, textAlign: "center" }}>No named users yet</div>
          )}
        </div>
      </div>

      {/* Members */}
      {(() => {
        const filteredMembers = memberSearch.trim()
          ? members.filter((m) => (m.user_metadata?.username || "").toLowerCase().includes(memberSearch.toLowerCase()))
          : members;
        const sortedMembers = [...filteredMembers].sort((a, b) => {
          if (memberSortBy === "joined_desc") return new Date(b.created_at || 0) - new Date(a.created_at || 0);
          if (memberSortBy === "joined_asc") return new Date(a.created_at || 0) - new Date(b.created_at || 0);
          if (memberSortBy === "name") return (a.user_metadata?.username || "").localeCompare(b.user_metadata?.username || "");
          if (memberSortBy === "mod") { const rank = r => r === "admin" ? 2 : r === "mod" ? 1 : 0; return rank(b.user_metadata?.role) - rank(a.user_metadata?.role); }
          return 0;
        });
        return (
          <div className="content-card" style={{ padding: 0, overflow: "hidden", marginTop: 16 }}>
            <div style={{ padding: "14px 20px", borderBottom: "1px solid #2e303a", display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
              <h3 style={{ margin: 0, color: "#f8fafc", fontSize: 16, fontWeight: 700, marginRight: "auto" }}>
                Members <span style={{ color: "#64748b", fontWeight: 500, fontSize: 13 }}>{sortedMembers.length}</span>
              </h3>
              <input
                placeholder="Search members…"
                value={memberSearch}
                onChange={(e) => setMemberSearch(e.target.value)}
                style={{ padding: "7px 12px", borderRadius: 10, border: "1px solid #3f4756", background: "#0f1117", color: "#f8fafc", fontSize: 16, width: 180 }}
              />
              <select
                value={memberSortBy}
                onChange={(e) => setMemberSortBy(e.target.value)}
                style={{ padding: "7px 12px", borderRadius: 10, border: "1px solid #374151", background: "#1f2937", color: "#dbe4ee", fontSize: 13, cursor: "pointer" }}
              >
                <option value="joined_desc">Newest first</option>
                <option value="joined_asc">Oldest first</option>
                <option value="name">Name A–Z</option>
                <option value="mod">Mods first</option>
              </select>
            </div>
            <div style={{ display: "flex", flexDirection: "column", maxHeight: 480, overflowY: "auto" }}>
              {sortedMembers.length === 0 && (
                <div style={{ padding: "32px 20px", color: "#64748b", fontSize: 14, textAlign: "center" }}>No registered members yet</div>
              )}
              {sortedMembers.map((m, i) => {
                const mUsername = m.user_metadata?.username || "";
                const mBrowserId = browserIdByUsername[mUsername] || null;
                const mAsUser = mBrowserId ? { browser_id: mBrowserId, username: mUsername } : null;
                const banned = mAsUser ? isBanned(mAsUser) : false;
                const jailedMember = mAsUser ? isJailed(mAsUser) : false;
                const mRole = m.user_metadata?.role || "user";
                const isMod = mRole === "mod";
                const isMemberAdmin = mRole === "admin";
                const isStaff = isMod || isMemberAdmin;
                const rowBg = banned ? "rgba(248,113,113,0.04)" : jailedMember ? "rgba(251,191,36,0.04)" : "transparent";
                const rolePill = isMemberAdmin
                  ? { label: "🐧 ADMIN", color: "#fb923c", bg: "rgba(251,146,60,0.12)" }
                  : isMod
                  ? { label: "🐦 MOD", color: "#c084fc", bg: "rgba(192,132,252,0.12)" }
                  : { label: "🐤 MEMBER", color: "#4ade80", bg: "rgba(74,222,128,0.1)" };
                return (
                  <div
                    key={m.id}
                    style={{ padding: "12px 16px", borderBottom: i < sortedMembers.length - 1 ? "1px solid #2e303a" : "none", background: rowBg }}
                  >
                    {/* Info row */}
                    <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 10 }}>
                      <div style={{ width: 32, height: 32, borderRadius: "50%", background: isStaff ? "#c084fc" : getUserColor(m.id, mUsername), display: "flex", alignItems: "center", justifyContent: "center", fontSize: 13, fontWeight: 800, color: "#0f1117", flexShrink: 0 }}>
                        {(mUsername || "?")?.[0]?.toUpperCase()}
                      </div>
                      <div style={{ flex: 1, minWidth: 0 }}>
                        <div style={{ display: "flex", alignItems: "center", gap: 6, flexWrap: "wrap" }}>
                          <UserPill
                            record={{ is_admin: isMemberAdmin, is_mod: isMod && !isMemberAdmin, username: mUsername || "—", browser_id: m.id }}
                            name={mUsername || "—"}
                            color={getUserColor(m.id, mUsername)}
                          />
                          {banned && <span style={{ fontSize: 10, fontWeight: 700, color: "#f87171", background: "rgba(248,113,113,0.12)", padding: "1px 6px", borderRadius: 999 }}>BANNED</span>}
                          {jailedMember && !banned && <span style={{ fontSize: 10, fontWeight: 700, color: "#fbbf24", background: "rgba(251,191,36,0.12)", padding: "1px 6px", borderRadius: 999 }}>CAGED</span>}
                        </div>
                        <div style={{ color: "#475569", fontSize: 11, marginTop: 1 }}>
                          Joined {timeAgo(m.created_at)}{mBrowserId ? ` · ${mBrowserId}` : ""}
                        </div>
                      </div>
                    </div>
                    {/* Action row */}
                    <div style={{ display: "flex", gap: 6 }}>
                      {mAsUser && (
                        <>
                          <button onClick={() => toggleJail(mAsUser)} style={{ flex: 1, padding: "7px 4px", borderRadius: 10, border: "none", background: jailedMember ? "#78350f" : "#451a03", color: jailedMember ? "#fde68a" : "#fbbf24", fontWeight: 700, cursor: "pointer", fontSize: 12 }}>
                            {jailedMember ? "Uncage" : "🪹 Cage"}
                          </button>
                          <button onClick={() => toggleBan(mAsUser)} style={{ flex: 1, padding: "7px 4px", borderRadius: 10, border: "none", background: banned ? "#1f2937" : "#7f1d1d", color: banned ? "#f8fafc" : "#fca5a5", fontWeight: 700, cursor: "pointer", fontSize: 12 }}>
                            {banned ? "Unban" : "Ban"}
                          </button>
                        </>
                      )}
                      {isAdmin && (
                        <button
                          onClick={async () => {
                            const next = isMemberAdmin ? "mod" : isMod ? "user" : "mod";
                            const headers = getAuthHeader();
                            await fetch("https://daboysforumip.coldbrainarchive.workers.dev/update-member", { method: "POST", headers: { "Content-Type": "application/json", ...headers }, body: JSON.stringify({ user_id: m.id, role: next }) });
                            load();
                          }}
                          style={{ flex: 1, padding: "7px 4px", borderRadius: 10, border: "none", background: isStaff ? "#1f2937" : "#c084fc", color: isStaff ? "#f8fafc" : "#14081d", fontWeight: 700, fontSize: 12, cursor: "pointer" }}
                        >
                          {isMemberAdmin ? "→ Mod" : isMod ? "Demote" : "→ Mod"}
                        </button>
                      )}
                      {isAdmin && isMod && (
                        <button
                          onClick={async () => {
                            const headers = getAuthHeader();
                            await fetch("https://daboysforumip.coldbrainarchive.workers.dev/update-member", { method: "POST", headers: { "Content-Type": "application/json", ...headers }, body: JSON.stringify({ user_id: m.id, role: "admin" }) });
                            load();
                          }}
                          style={{ flex: 1, padding: "7px 4px", borderRadius: 10, border: "none", background: "#fb923c", color: "#14081d", fontWeight: 700, fontSize: 12, cursor: "pointer" }}
                        >
                          → Admin
                        </button>
                      )}
                      <button
                        onClick={async () => {
                          if (!confirm(`Delete ${mUsername || "this member"}? This cannot be undone.`)) return;
                          const headers = getAuthHeader();
                          await fetch("https://daboysforumip.coldbrainarchive.workers.dev/delete-member", { method: "POST", headers: { "Content-Type": "application/json", ...headers }, body: JSON.stringify({ user_id: m.id }) });
                          load();
                        }}
                        style={{ flex: 1, padding: "7px 4px", borderRadius: 10, border: "1px solid #374151", background: "transparent", color: "#f87171", fontWeight: 700, fontSize: 12, cursor: "pointer" }}
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        );
      })()}

      {/* Bots */}
      <div className="content-card" style={{ padding: 0, overflow: "hidden", marginTop: 16 }}>
        <div style={{ padding: "14px 20px", borderBottom: "1px solid #2e303a" }}>
          <h3 style={{ margin: 0, color: "#f8fafc", fontSize: 16, fontWeight: 700 }}>
            Bots <span style={{ color: "#64748b", fontWeight: 500, fontSize: 13 }}>{bots.length}</span>
          </h3>
        </div>
        <div style={{ display: "flex", flexDirection: "column" }}>
          {bots.length === 0 && (
            <div style={{ padding: "32px 20px", color: "#64748b", fontSize: 14, textAlign: "center" }}>No bot activity yet</div>
          )}
          {bots.map((u, i) => {
            const botIcons = { NewsBot: "🗳️", ScienceBot: "🔬", NatureBot: "🌿", SportsBot: "🏈" };
            return (
              <div key={u.browser_id} style={{ padding: "12px 16px", borderBottom: i < bots.length - 1 ? "1px solid #2e303a" : "none" }}>
                <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                  <div style={{ width: 32, height: 32, borderRadius: "50%", background: "#1e3a5f", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 15, flexShrink: 0 }}>
                    {botIcons[u.username] || "🤖"}
                  </div>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                      <UserPill record={{ browser_id: u.browser_id, username: u.username }} name={u.username} color="#38bdf8" />
                    </div>
                    <div style={{ color: "#64748b", fontSize: 11, marginTop: 1 }}>
                      {u.joined_at ? `last active ${timeAgo(u.joined_at)} · ` : ""}{u.browser_id}
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Archive */}
      <div className="content-card" style={{ padding: 0, overflow: "hidden", marginTop: 16 }}>
        <div
          style={{ padding: "14px 20px", borderBottom: archiveExpanded ? "1px solid #2e303a" : "none", display: "flex", alignItems: "center", gap: 10, cursor: "pointer" }}
          onClick={() => setArchiveExpanded(v => !v)}
        >
          <h3 style={{ margin: 0, color: "#f8fafc", fontSize: 16, fontWeight: 700, flex: 1 }}>
            Archive <span style={{ color: "#64748b", fontWeight: 500, fontSize: 13 }}>{archivedPosts.length}</span>
          </h3>
          {archiveExpanded && (
            <input
              placeholder="Search archive…"
              value={archiveSearch}
              onChange={e => { e.stopPropagation(); setArchiveSearch(e.target.value); }}
              onClick={e => e.stopPropagation()}
              style={{ padding: "6px 12px", borderRadius: 10, border: "1px solid #3f4756", background: "#0f1117", color: "#f8fafc", fontSize: 13, width: 180 }}
            />
          )}
          <span style={{ color: "#64748b", fontSize: 13 }}>{archiveExpanded ? "▲" : "▼"}</span>
        </div>

        {archiveExpanded && (
          <div style={{ display: "flex", flexDirection: "column", maxHeight: 520, overflowY: "auto" }}>
            {archivedPosts.length === 0 && (
              <div style={{ padding: "32px 20px", color: "#64748b", fontSize: 14, textAlign: "center" }}>No deleted posts</div>
            )}
            {archivedPosts
              .filter(p => !archiveSearch.trim() || p.title?.toLowerCase().includes(archiveSearch.toLowerCase()) || (p.username || "").toLowerCase().includes(archiveSearch.toLowerCase()))
              .map((p, i, arr) => {
                const boardName = getBoardNameFromPost(p);
                const board = BOARDS.find(b => b.name === boardName);
                return (
                  <div key={p.id} style={{ padding: "12px 16px", borderBottom: i < arr.length - 1 ? "1px solid #2e303a" : "none", display: "flex", alignItems: "center", gap: 12 }}>
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ color: "#f8fafc", fontWeight: 600, fontSize: 14, marginBottom: 3, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                        {p.title || "—"}
                      </div>
                      <div style={{ color: "#64748b", fontSize: 11, display: "flex", alignItems: "center", gap: 6, flexWrap: "wrap" }}>
                        {board && <span style={{ color: "#94a3b8" }}>{board.icon} {board.name}</span>}
                        {board && <span>·</span>}
                        <UserPill record={p} name={p.username || `Anon #${shortId(p.browser_id)}`} color={getUserColor(p.browser_id, p.username)} />
                        <span>·</span>
                        <span>{timeAgo(p.created_at)}</span>
                      </div>
                    </div>
                    <div style={{ display: "flex", gap: 6, flexShrink: 0 }}>
                      <Link
                        to={`/post/${p.id}`}
                        style={{ padding: "6px 12px", borderRadius: 8, border: "1px solid #374151", background: "#1f2937", color: "#f8fafc", fontWeight: 600, fontSize: 12, textDecoration: "none" }}
                      >
                        View
                      </Link>
                      <button
                        onClick={async () => {
                          await modAction({ type: "restore_post", post_id: p.id });
                          load();
                        }}
                        style={{ padding: "6px 12px", borderRadius: 8, border: "none", background: "#14532d", color: "#4ade80", fontWeight: 600, fontSize: 12, cursor: "pointer" }}
                      >
                        Restore
                      </button>
                    </div>
                  </div>
                );
              })}
          </div>
        )}
      </div>

      {/* Bot Panel (admin only) */}
      {isAdmin && <div className="content-card" style={{ padding: 0, overflow: "hidden", marginTop: 16 }}>
        {/* Header */}
        <div
          onClick={() => setBotPanelOpen(v => !v)}
          style={{ padding: "14px 20px", borderBottom: botPanelOpen ? "1px solid #2e303a" : "none", display: "flex", alignItems: "center", gap: 10, cursor: "pointer", userSelect: "none" }}
        >
          <span style={{ color: "#475569", fontSize: 12 }}>{botPanelOpen ? "▾" : "▸"}</span>
          <h3 style={{ margin: 0, color: "#f8fafc", fontSize: 16, fontWeight: 700, flex: 1 }}>Bot</h3>
          {botConfig && (
            <span style={{ fontSize: 12, color: botConfig.enabled ? "#4ade80" : "#f87171", fontWeight: 600 }}>
              {botConfig.enabled ? "● ACTIVE" : "● PAUSED"}
            </span>
          )}
          {/* Stop click-through on buttons inside the header */}
          <div onClick={e => e.stopPropagation()} style={{ display: "flex", gap: 8 }}>
            <button
              onClick={refreshLogs}
              disabled={botLogsLoading}
              style={{ padding: "7px 14px", borderRadius: 10, border: "1px solid #374151", background: "#1f2937", color: "#94a3b8", fontWeight: 600, fontSize: 13, cursor: botLogsLoading ? "not-allowed" : "pointer", opacity: botLogsLoading ? 0.6 : 1 }}
            >
              {botLogsLoading ? "Loading…" : "↻ Refresh"}
            </button>
            <button
              onClick={triggerBot}
              disabled={botTriggering}
              style={{ padding: "7px 18px", borderRadius: 10, border: "none", background: "#c084fc", color: "#14081d", fontWeight: 700, fontSize: 13, cursor: botTriggering ? "not-allowed" : "pointer", opacity: botTriggering ? 0.7 : 1 }}
            >
              {botTriggering ? "Triggering…" : "▶ Run Now"}
            </button>
          </div>
        </div>

        {botPanelOpen && (
          <div style={{ display: "flex", flexDirection: "column" }}>

            {/* ── Run Logs (collapsible, scrollable) ── */}
            <div style={{ borderBottom: "1px solid #2e303a" }}>
              <div
                onClick={() => setBotLogsOpen(v => !v)}
                style={{ padding: "12px 20px", display: "flex", alignItems: "center", gap: 8, cursor: "pointer", userSelect: "none" }}
              >
                <span style={{ color: "#475569", fontSize: 10 }}>{botLogsOpen ? "▾" : "▸"}</span>
                <span style={{ color: "#94a3b8", fontSize: 11, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.05em", flex: 1 }}>Run Logs</span>
                <span style={{ color: "#374151", fontSize: 11 }}>({botLogs.length})</span>
              </div>
              {botLogsOpen && (
                <div style={{ padding: "0 20px 16px", maxHeight: 600, overflowY: "auto", display: "flex", flexDirection: "column", gap: 8 }}>
                  {botLogs.length === 0 && (
                    <div style={{ color: "#64748b", fontSize: 13 }}>No runs logged yet.</div>
                  )}
                  {botLogs.map(log => {
                    const isExpanded = expandedLog === log.id;
                    const startTime = new Date(log.started_at);
                    const endTime = log.finished_at ? new Date(log.finished_at) : null;
                    const duration = endTime ? Math.round((endTime - startTime) / 1000) : null;
                    const statusColor = log.status === "done" ? "#4ade80" : log.status === "running" ? "#facc15" : "#f87171";
                    return (
                      <div key={log.id} style={{ background: "#1a1c24", borderRadius: 10, border: "1px solid #2e303a", overflow: "hidden" }}>
                        <div style={{ padding: "10px 14px", display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
                          <div
                            onClick={() => setExpandedLog(isExpanded ? null : log.id)}
                            style={{ display: "flex", alignItems: "center", gap: 10, flex: 1, cursor: "pointer", flexWrap: "wrap", minWidth: 0 }}
                          >
                            <span style={{ color: statusColor, fontWeight: 700, fontSize: 12 }}>● {log.status.toUpperCase()}</span>
                            <span style={{ color: "#94a3b8", fontSize: 12 }}>{startTime.toLocaleString()}</span>
                            <span style={{ color: "#64748b", fontSize: 12 }}>{log.run_type === "first_run" ? "First Run" : "Scheduled"}</span>
                            {duration !== null && <span style={{ color: "#64748b", fontSize: 12 }}>{duration}s</span>}
                            <span style={{ color: "#4ade80", fontWeight: 700, fontSize: 13 }}>+{log.posted} posted</span>
                            <span style={{ color: "#64748b", fontSize: 11 }}>{isExpanded ? "▲" : "▼"}</span>
                          </div>
                          <button
                            onClick={() => deleteLog(log.id)}
                            title="Delete log"
                            style={{ background: "none", border: "none", color: "#374151", cursor: "pointer", fontSize: 16, padding: "0 2px", lineHeight: 1, flexShrink: 0 }}
                          >×</button>
                        </div>

                        {isExpanded && (
                          <div style={{ padding: "0 14px 14px", borderTop: "1px solid #2e303a", display: "flex", flexDirection: "column", gap: 12 }}>
                            <div style={{ display: "flex", gap: 12, flexWrap: "wrap", paddingTop: 12 }}>
                              {[
                                { label: "Posted", value: log.posted, color: "#4ade80" },
                                { label: "Skipped (seen)", value: log.skipped_seen, color: "#94a3b8" },
                                { label: "Bad title", value: log.skipped_bad_title, color: "#94a3b8" },
                                { label: "Post failed", value: log.post_failed, color: log.post_failed > 0 ? "#f87171" : "#94a3b8" },
                                { label: "Feed errors", value: (log.feed_errors || []).length, color: (log.feed_errors || []).length > 0 ? "#f87171" : "#94a3b8" },
                              ].map(({ label, value, color }) => (
                                <div key={label} style={{ background: "#12141b", borderRadius: 8, padding: "8px 14px", minWidth: 80 }}>
                                  <div style={{ color: "#64748b", fontSize: 10, fontWeight: 700, textTransform: "uppercase", marginBottom: 4 }}>{label}</div>
                                  <div style={{ color, fontWeight: 700, fontSize: 18 }}>{value}</div>
                                </div>
                              ))}
                            </div>

                            {(log.posted_articles || []).length > 0 && (
                              <div>
                                <div style={{ color: "#64748b", fontSize: 11, fontWeight: 700, textTransform: "uppercase", marginBottom: 6 }}>Posted ({log.posted_articles.length})</div>
                                <div style={{ display: "flex", flexDirection: "column", gap: 4, maxHeight: 300, overflowY: "auto", paddingRight: 4 }}>
                                  {log.posted_articles.map((a, i) => (
                                    <div key={i} style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 12 }}>
                                      <span style={{ color: "#64748b", minWidth: 80 }}>[{a.board}]</span>
                                      <a href={a.url} target="_blank" rel="noopener noreferrer" style={{ color: "#c084fc", textDecoration: "none" }}>{a.title}</a>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}

                            {(log.feed_errors || []).length > 0 && (
                              <div>
                                <div style={{ color: "#f87171", fontSize: 11, fontWeight: 700, textTransform: "uppercase", marginBottom: 6 }}>Feed Errors</div>
                                <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
                                  {log.feed_errors.map((e, i) => (
                                    <div key={i} style={{ color: "#f87171", fontSize: 12, fontFamily: "monospace", background: "#12141b", padding: "4px 8px", borderRadius: 6 }}>{e}</div>
                                  ))}
                                </div>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}
            </div>

            {/* ── Settings ── */}
            {botConfig && (
              <div style={{ padding: 20, display: "flex", flexDirection: "column", gap: 20 }}>

                {/* Enable toggle + Posts per link + interval */}
                <div style={{ display: "flex", alignItems: "flex-end", gap: 16, flexWrap: "wrap" }}>
                  <label style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer", paddingBottom: 8 }}>
                    <input
                      type="checkbox"
                      checked={botConfig.enabled}
                      onChange={e => setBotConfig(c => ({ ...c, enabled: e.target.checked }))}
                      style={{ width: 16, height: 16, cursor: "pointer" }}
                    />
                    <span style={{ color: "#f8fafc", fontWeight: 700, fontSize: 14 }}>Bots enabled</span>
                  </label>
                  <div>
                    <div style={{ color: "#94a3b8", fontSize: 11, fontWeight: 700, marginBottom: 6, textTransform: "uppercase", letterSpacing: "0.05em" }}>Posts per link</div>
                    <select
                      value={botConfig.max_per_feed || 1}
                      onChange={e => setBotConfig(c => ({ ...c, max_per_feed: Number(e.target.value) }))}
                      style={{ padding: "8px 12px", borderRadius: 8, border: "1px solid #374151", background: "#1f2937", color: "#f8fafc", fontSize: 13 }}
                    >
                      {[1,2,3,4,5].map(n => <option key={n} value={n}>{n}</option>)}
                    </select>
                  </div>
                  <div>
                    <div style={{ color: "#94a3b8", fontSize: 11, fontWeight: 700, marginBottom: 6, textTransform: "uppercase", letterSpacing: "0.05em" }}>Post interval</div>
                    <select
                      value={botConfig.interval_hours}
                      onChange={e => setBotConfig(c => ({ ...c, interval_hours: Number(e.target.value) }))}
                      style={{ padding: "8px 12px", borderRadius: 8, border: "1px solid #374151", background: "#1f2937", color: "#f8fafc", fontSize: 13 }}
                    >
                      <option value={0.25}>Every 15 min</option>
                      <option value={0.5}>Every 30 min</option>
                      <option value={1}>Every 1 hour</option>
                      <option value={2}>Every 2 hours</option>
                      <option value={6}>Every 6 hours</option>
                      <option value={12}>Every 12 hours</option>
                      <option value={24}>Every 24 hours</option>
                    </select>
                  </div>
                </div>

                {/* Feeds (collapsible) */}
                <div>
                  <div
                    onClick={() => setBotFeedsOpen(v => !v)}
                    style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer", userSelect: "none", marginBottom: botFeedsOpen ? 10 : 0 }}
                  >
                    <span style={{ color: "#475569", fontSize: 10 }}>{botFeedsOpen ? "▾" : "▸"}</span>
                    <span style={{ color: "#94a3b8", fontSize: 11, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.05em" }}>
                      RSS Feeds
                    </span>
                    <span style={{ color: "#374151", fontSize: 11 }}>({(botConfig.feeds || []).filter(f => f.enabled !== false).length} / {(botConfig.feeds || []).length})</span>
                  </div>
                  {botFeedsOpen && [...CONTINENTS, ""].map(continent => {
                    const groupEntries = botConfig.feeds.map((f, i) => ({ feed: f, i })).filter(({ feed }) => (feed.continent || "") === continent);
                    const label = continent || "Unassigned";
                    const isExpanded = feedGroupExpanded[continent] !== false;
                    return (
                      <div key={continent} style={{ marginBottom: 12 }}>
                        <div
                          onClick={() => setFeedGroupExpanded(s => ({ ...s, [continent]: !isExpanded }))}
                          style={{ display: "flex", alignItems: "center", gap: 6, cursor: "pointer", marginBottom: isExpanded ? 8 : 0, userSelect: "none" }}
                        >
                          <span style={{ color: "#475569", fontSize: 10 }}>{isExpanded ? "▾" : "▸"}</span>
                          <span style={{ color: "#64748b", fontSize: 11, fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.04em" }}>{label}</span>
                          <span style={{ color: "#374151", fontSize: 11 }}>({groupEntries.length})</span>
                        </div>
                        {isExpanded && (
                          <>
                            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                              {groupEntries.map(({ feed, i }) => (
                                <div
                                  key={i}
                                  draggable
                                  onDragStart={() => { feedDragIndex.current = i; }}
                                  onDragOver={e => {
                                    e.preventDefault();
                                    if (feedDragIndex.current === null || feedDragIndex.current === i) return;
                                    const draggedFeed = botConfig.feeds[feedDragIndex.current];
                                    if ((draggedFeed.continent || "") !== (feed.continent || "")) return;
                                    setBotConfig(c => {
                                      const feeds = [...c.feeds];
                                      const [moved] = feeds.splice(feedDragIndex.current, 1);
                                      feeds.splice(i, 0, moved);
                                      feedDragIndex.current = i;
                                      return { ...c, feeds };
                                    });
                                  }}
                                  onDragEnd={() => { feedDragIndex.current = null; }}
                                  style={{ display: "flex", alignItems: "center", gap: 8, background: "#0f1117", padding: "10px 12px", borderRadius: 10, border: `1px solid ${feed.enabled !== false ? "#2e303a" : "#1c1e26"}`, opacity: feed.enabled !== false ? 1 : 0.5, cursor: "grab" }}
                                >
                                  <span style={{ color: "#374151", fontSize: 14, cursor: "grab", flexShrink: 0, userSelect: "none" }}>⠿</span>
                                  <input
                                    type="checkbox"
                                    checked={feed.enabled !== false}
                                    onChange={e => setBotConfig(c => ({ ...c, feeds: c.feeds.map((f, j) => j === i ? { ...f, enabled: e.target.checked } : f) }))}
                                    style={{ flexShrink: 0, cursor: "pointer" }}
                                  />
                                  <input
                                    value={feed.url}
                                    onChange={e => setBotConfig(c => ({ ...c, feeds: c.feeds.map((f, j) => j === i ? { ...f, url: e.target.value } : f) }))}
                                    placeholder="RSS feed URL"
                                    style={{ flex: 1, background: "transparent", border: "none", color: "#94a3b8", fontSize: 12, minWidth: 0, outline: "none" }}
                                  />
                                  <select
                                    value={feed.board || ""}
                                    onChange={e => setBotConfig(c => ({ ...c, feeds: c.feeds.map((f, j) => j === i ? { ...f, board: e.target.value } : f) }))}
                                    style={{ padding: "3px 6px", borderRadius: 6, border: "1px solid #374151", background: "#1f2937", color: feed.board ? "#f8fafc" : "#64748b", fontSize: 11, flexShrink: 0 }}
                                  >
                                    <option value="">Board</option>
                                    {BOARDS.filter(b => !b.virtual && b.slug !== "cage").map(b => (
                                      <option key={b.slug} value={b.slug}>{b.icon} {b.name}</option>
                                    ))}
                                  </select>
                                  <select
                                    value={feed.continent || ""}
                                    onChange={e => setBotConfig(c => ({ ...c, feeds: c.feeds.map((f, j) => j === i ? { ...f, continent: e.target.value || undefined, country: undefined } : f) }))}
                                    style={{ padding: "3px 6px", borderRadius: 6, border: "1px solid #374151", background: "#1f2937", color: feed.continent ? "#c084fc" : "#64748b", fontSize: 11, flexShrink: 0 }}
                                  >
                                    <option value="">Continent</option>
                                    {CONTINENTS.map(c => <option key={c} value={c}>{c}</option>)}
                                  </select>
                                  <select
                                    value={feed.country || ""}
                                    onChange={e => setBotConfig(c => ({ ...c, feeds: c.feeds.map((f, j) => j === i ? { ...f, country: e.target.value || undefined } : f) }))}
                                    style={{ padding: "3px 6px", borderRadius: 6, border: "1px solid #374151", background: "#1f2937", color: feed.country ? "#c084fc" : "#64748b", fontSize: 11, flexShrink: 0 }}
                                  >
                                    <option value="">Country</option>
                                    {COUNTRIES_WITH_FLAGS.map(c => <option key={c.name} value={c.name}>{c.flag} {c.name}</option>)}
                                  </select>
                                  <button
                                    onClick={() => setBotConfig(c => ({ ...c, feeds: c.feeds.filter((_, j) => j !== i) }))}
                                    style={{ background: "none", border: "none", color: "#f87171", cursor: "pointer", fontSize: 18, padding: "0 2px", flexShrink: 0, lineHeight: 1 }}
                                  >×</button>
                                </div>
                              ))}
                            </div>
                            <button
                              onClick={() => setBotConfig(c => ({ ...c, feeds: [...c.feeds, { url: "", enabled: true, continent: continent || undefined }] }))}
                              style={{ marginTop: 8, padding: "6px 12px", borderRadius: 8, border: "1px dashed #374151", background: "transparent", color: "#64748b", fontSize: 12, cursor: "pointer", width: "100%" }}
                            >
                              + Add {label} feed
                            </button>
                          </>
                        )}
                      </div>
                    );
                  })}
                </div>

                <button
                  onClick={saveBotConfig}
                  disabled={savingBotConfig}
                  style={{ alignSelf: "flex-start", padding: "8px 24px", borderRadius: 10, border: "none", background: "#c084fc", color: "#14081d", fontWeight: 700, fontSize: 13, cursor: savingBotConfig ? "not-allowed" : "pointer", opacity: savingBotConfig ? 0.7 : 1 }}
                >
                  {savingBotConfig ? "Saving…" : "Save Settings"}
                </button>

              </div>
            )}

          </div>
        )}
      </div>}

    </div>
  );
}
// ==============================
// USER PANEL
// ==============================
function UserPanel({ user, userRole, modName, browseUsername, lastMemberUsername, onClose, onLogout, onLogin }) {
  const [tab, setTab] = useState("notifications");
  const [newPassword, setNewPassword] = useState("");
  const [posts, setPosts] = useState([]);
  const [notifs, setNotifs] = useState([]);
  const [notifLoading, setNotifLoading] = useState(true);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isSignUp, setIsSignUp] = useState(false);
  const [generatedUsername, setGeneratedUsername] = useState(() => generateBirdUsername());
  const [authLoading, setAuthLoading] = useState(false);
  const unseenThreshold = useRef(localStorage.getItem("notif_last_seen") || new Date(0).toISOString());

  // Stamp notif_last_seen on open so the next badge count starts from now
  useEffect(() => {
    localStorage.setItem("notif_last_seen", new Date().toISOString());
  }, []);

  const isMod = !!user && (userRole === "mod" || userRole === "admin");
  const isMember = !!user && !isMod;

  const browserId = getBrowserId();
  const avatarColor = isMod ? "#c084fc" : (browseUsername ? getUserColor(browserId, browseUsername) : "#c084fc");
  const displayName = isMod ? modName : (browseUsername || "Guest");
  const roleLabel = userRole === "admin" ? "Administrator" : isMod ? "Moderator" : (isMember ? "Member" : browseUsername ? "Anonymous" : "Guest");

  // Fetch posts
  useEffect(() => {
    (async () => {
      const params = new URLSearchParams({ browser_id: browserId });
      if (isMod && user) params.set("mod_user_id", user.id);
      else if (browseUsername) params.set("username", browseUsername);
      if (lastMemberUsername) params.set("exclude_username", lastMemberUsername);
      const res = await fetch(`${WORKER_URL}/my-posts?${params}`, { headers: getOptionalAuthHeader() });
      const data = res.ok ? await res.json() : {};
      setPosts(data.posts || []);
    })();
  }, [browseUsername, isMod, isMember]);

  // Fetch notifs
  useEffect(() => {
    if (tab !== "notifications") return;
    setNotifLoading(true);
    (async () => {
      const params = new URLSearchParams({ browser_id: browserId });
      if (isMod && user) params.set("mod_user_id", user.id);
      else if (browseUsername) params.set("username", browseUsername);
      if (lastMemberUsername) params.set("exclude_username", lastMemberUsername);
      const res = await fetch(`${WORKER_URL}/notifications?${params}`, { headers: getOptionalAuthHeader() });
      const data = res.ok ? await res.json() : {};
      setNotifs(data.notifs || []);
      setNotifLoading(false);
    })();
  }, [tab, user, browseUsername]);

  const updatePassword = async () => {
    if (!newPassword) return;
    try {
      const res = await fetch(`${WORKER_URL}/update-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...getAuthHeader() },
        body: JSON.stringify({ newPassword })
      });
      const data = await res.json();
      if (!res.ok) return alert(data.error || "Failed to update password");
      alert("Password updated 🔑");
      setNewPassword("");
    } catch (err) { alert(err.message); }
  };

  const handleAuth = async () => {
    if (isSignUp) {
      if (!password) return;
    } else {
      if (!username.trim() || !password) return;
    }
    setAuthLoading(true);
    if (isSignUp) {
      const signUpUsername = generatedUsername;
      try {
        const res = await fetch(`${WORKER_URL}/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username: signUpUsername, password, browser_id: getBrowserId() })
        });
        const data = await res.json();
        setAuthLoading(false);
        if (!res.ok) { alert(data.error || "Registration failed"); return; }
        localStorage.setItem("auth_token", data.token);
        localStorage.setItem("auth_user", JSON.stringify(data.user));
        onLogin(data.user, data.user.role || "user", signUpUsername);
        onClose();
      } catch (err) { setAuthLoading(false); alert(err.message); }
    } else {
      try {
        const res = await fetch(`${WORKER_URL}/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username: username.trim(), password })
        });
        const data = await res.json();
        setAuthLoading(false);
        if (!res.ok) { alert("Invalid username or password"); return; }
        localStorage.setItem("auth_token", data.token);
        localStorage.setItem("auth_user", JSON.stringify(data.user));
        const role = data.user.role || "user";
        const memberUsername = data.user.username || null;
        onLogin(data.user, role, memberUsername);
        onClose();
      } catch (err) { setAuthLoading(false); alert(err.message); }
    }
  };

  const filtered = notifs;

  const TABS = [
    { id: "notifications", label: "Notifications" },
    { id: "posts", label: "Posts" },
    { id: "account", label: "Account" }
  ];
  const tabIds = TABS.map((t) => t.id);

  const swipeRef = useRef({ startX: 0, startY: 0 });
  const handleSwipeStart = (e) => {
    swipeRef.current.startX = e.touches[0].clientX;
    swipeRef.current.startY = e.touches[0].clientY;
  };
  const handleSwipeEnd = (e) => {
    const dx = e.changedTouches[0].clientX - swipeRef.current.startX;
    const dy = e.changedTouches[0].clientY - swipeRef.current.startY;
    if (Math.abs(dx) < 40 || Math.abs(dx) < Math.abs(dy) * 1.2) return;
    const idx = tabIds.indexOf(tab);
    if (dx < 0) {
      // swipe left → next tab
      if (idx < tabIds.length - 1) setTab(tabIds[idx + 1]);
    } else {
      // swipe right → previous tab, or close if already on first
      if (idx === 0) { onClose(); } else { setTab(tabIds[idx - 1]); }
    }
  };

  return (
    <>
      <div onClick={onClose} style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.55)", zIndex: 50, backdropFilter: "blur(3px)" }} />
      <div style={{ position: "fixed", top: 0, right: 0, bottom: 0, width: "min(420px, 100vw)", background: "linear-gradient(180deg, #1b1d24 0%, #14161c 100%)", borderLeft: "1px solid #2e303a", zIndex: 51, display: "flex", flexDirection: "column", boxShadow: "-20px 0 60px rgba(0,0,0,0.5)" }}>
        {/* Header */}
        <div style={{ padding: "14px 18px", borderBottom: "1px solid #2e303a", display: "flex", alignItems: "center", justifyContent: "center", position: "relative" }}>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 4 }}>
            <UserPill
              record={{ is_admin: userRole === "admin", is_mod: userRole === "mod", username: displayName, browser_id: browserId }}
              name={displayName}
              color={avatarColor}
            />
            <div style={{ color: "#64748b", fontSize: 12 }}>{roleLabel}</div>
          </div>
          <button onClick={onClose} style={{ position: "absolute", right: 18, top: "50%", transform: "translateY(-50%)", width: 30, height: 30, borderRadius: "50%", border: "none", background: "#1f2937", color: "#94a3b8", cursor: "pointer", fontSize: 14, display: "flex", alignItems: "center", justifyContent: "center" }}>✕</button>
        </div>

        {/* Tabs */}
        <div style={{ display: "flex", borderBottom: "1px solid #2e303a", flexShrink: 0 }}>
          {TABS.map((t) => (
            <button key={t.id} onClick={() => setTab(t.id)} style={{ flex: 1, padding: "10px 8px", border: "none", borderBottom: tab === t.id ? "2px solid #c084fc" : "2px solid transparent", marginBottom: -1, background: "transparent", color: tab === t.id ? "#f8fafc" : "#64748b", fontWeight: tab === t.id ? 700 : 500, fontSize: 13, cursor: "pointer" }}>
              {t.label}
            </button>
          ))}
        </div>

        {/* Content */}
        <div style={{ flex: 1, overflowY: "auto" }} onTouchStart={handleSwipeStart} onTouchEnd={handleSwipeEnd}>
          {tab === "notifications" && (
            <div style={{ display: "flex", flexDirection: "column" }}>
              {notifLoading ? (
                <div style={{ padding: 32, color: "#64748b", textAlign: "center", fontSize: 14 }}>Loading…</div>
              ) : filtered.length === 0 ? (
                <div style={{ padding: "48px 20px", color: "#64748b", textAlign: "center" }}>
                  <div style={{ fontSize: 36, marginBottom: 12 }}>🐦</div>
                  <div style={{ fontSize: 14, fontWeight: 600 }}>No notifications yet</div>
                  <div style={{ fontSize: 12, marginTop: 4 }}>Activity on your posts and comments shows up here</div>
                </div>
              ) : filtered.map((n) => {
                const isUnseen = !!n.time && n.time > unseenThreshold.current;
                return (
                  <Link key={n.id} to={n.postId ? `/post/${n.postId}${n.targetId ? `?highlight=${n.targetId}` : ""}` : "#"} onClick={onClose}
                    style={{ display: "flex", alignItems: "flex-start", gap: 12, padding: "12px 18px", textDecoration: "none", borderBottom: "1px solid #1a1c23", background: isUnseen ? "rgba(192,132,252,0.07)" : "transparent", borderLeft: isUnseen ? "2px solid #c084fc" : "2px solid transparent" }}
                    onMouseEnter={(e) => e.currentTarget.style.background = "#1f2028"}
                    onMouseLeave={(e) => e.currentTarget.style.background = isUnseen ? "rgba(192,132,252,0.07)" : "transparent"}
                  >
                    <div style={{ width: 36, height: 36, borderRadius: "50%", background: "#1f2937", border: "1px solid #2e303a", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16, flexShrink: 0 }}>{n.icon}</div>
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ color: "#e2e8f0", fontSize: 13, fontWeight: 600, lineHeight: 1.4 }}>{n.text}</div>
                      {n.subtext && <div style={{ color: "#94a3b8", fontSize: 12, marginTop: 1 }}>{n.subtext}</div>}
                      {n.preview && <div style={{ color: "#64748b", fontSize: 12, marginTop: 3, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{n.preview}</div>}
                      {n.time && <div style={{ color: "#475569", fontSize: 11, marginTop: 5 }}>{timeAgo(n.time)}</div>}
                    </div>
                  </Link>
                );
              })}
            </div>
          )}

          {tab === "posts" && (
            <div style={{ display: "flex", flexDirection: "column" }}>
              {posts.length === 0 ? (
                <div style={{ padding: "48px 20px", color: "#64748b", textAlign: "center" }}>
                  <div style={{ fontSize: 32, marginBottom: 10 }}>📝</div>
                  <div style={{ fontSize: 14, fontWeight: 600 }}>No posts yet</div>
                </div>
              ) : posts.map((p, i) => (
                <Link key={p.id} to={`/post/${p.id}`} onClick={onClose} style={{ display: "block", padding: "12px 18px", borderBottom: i < posts.length - 1 ? "1px solid #1a1c23" : "none", textDecoration: "none" }}
                  onMouseEnter={(e) => e.currentTarget.style.background = "#1f2028"}
                  onMouseLeave={(e) => e.currentTarget.style.background = "transparent"}
                >
                  <div style={{ color: "#e2e8f0", fontSize: 14, fontWeight: 600, marginBottom: 3 }}>{p.title}</div>
                  <div style={{ color: "#475569", fontSize: 12 }}>{p.board ? `${p.board} · ` : ""}{timeAgo(p.created_at)}</div>
                </Link>
              ))}
            </div>
          )}

          {tab === "account" && (
            <div style={{ padding: 20, display: "flex", flexDirection: "column", gap: 14 }}>
              {isMember && (
                <>
                  <div className="content-card" style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                    <div style={{ fontSize: 11, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em" }}>Username</div>
                    <div style={{ padding: "9px 12px", borderRadius: 10, border: "1px solid #2e303a", background: "#16171d", color: "#94a3b8", fontSize: 14 }}>@{browseUsername || "—"}</div>
                  </div>
                  <div className="content-card" style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                    <div style={{ fontSize: 11, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em" }}>Change Password</div>
                    <input type="password" placeholder="New password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} onKeyDown={(e) => e.key === "Enter" && updatePassword()} style={{ padding: "9px 12px", borderRadius: 10, border: "1px solid #3f4756", background: "#0f1117", color: "#f8fafc", fontSize: 16, width: "100%", boxSizing: "border-box" }} />
                    <button onClick={updatePassword} style={{ padding: "9px 14px", borderRadius: 10, border: "none", background: "#c084fc", color: "#14081d", fontWeight: 700, fontSize: 13, cursor: "pointer" }}>Update Password</button>
                  </div>
                  <button onClick={() => { onLogout(); onClose(); }} style={{ padding: "10px 16px", borderRadius: 12, border: "1px solid #374151", background: "transparent", color: "#94a3b8", fontWeight: 700, fontSize: 14, cursor: "pointer" }}>
                    🚪 Log out
                  </button>
                </>
              )}
              {isMod && (
                <>
                  <div className="content-card" style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                    <div style={{ fontSize: 11, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em" }}>Username</div>
                    <div style={{ padding: "9px 12px", borderRadius: 10, border: "1px solid #2e303a", background: "#16171d", color: "#94a3b8", fontSize: 14 }}>@{modName}</div>
                  </div>
                  <Link to="/mod" onClick={onClose} style={{ display: "block", padding: "10px 16px", borderRadius: 12, background: "#c084fc", color: "#14081d", fontWeight: 700, fontSize: 14, cursor: "pointer", textDecoration: "none", textAlign: "center" }}>
                    Open Mod Panel
                  </Link>
                  <button onClick={() => { onLogout(); onClose(); }} style={{ padding: "10px 16px", borderRadius: 12, border: "1px solid #374151", background: "transparent", color: "#94a3b8", fontWeight: 700, fontSize: 14, cursor: "pointer" }}>
                    🚪 Log out
                  </button>
                </>
              )}
              {!user && (
                <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                  <div style={{ fontSize: 12, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 2 }}>
                    {isSignUp ? "Create account" : "Sign in"}
                  </div>
                  {isSignUp ? (
                    <>
                      <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
                        <div style={{ fontSize: 11, color: "#64748b" }}>Your username (bird-assigned 🐦)</div>
                        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                          <div style={{ flex: 1, padding: "9px 12px", borderRadius: 10, border: "1px solid #2e303a", background: "#16171d", color: "#c084fc", fontSize: 14, fontWeight: 600, fontFamily: "monospace", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                            @{generatedUsername}
                          </div>
                          <button
                            onClick={() => setGeneratedUsername(generateBirdUsername())}
                            title="Generate a new username"
                            style={{ flexShrink: 0, padding: "9px 11px", borderRadius: 10, border: "1px solid #374151", background: "#1f2028", color: "#94a3b8", fontSize: 16, cursor: "pointer", lineHeight: 1 }}
                          >🔀</button>
                        </div>
                      </div>
                      <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} onKeyDown={(e) => e.key === "Enter" && handleAuth()} style={{ padding: "9px 12px", borderRadius: 10, border: "1px solid #3f4756", background: "#0f1117", color: "#f8fafc", fontSize: 16, width: "100%", boxSizing: "border-box" }} />
                    </>
                  ) : (
                    <input placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} style={{ padding: "9px 12px", borderRadius: 10, border: "1px solid #3f4756", background: "#0f1117", color: "#f8fafc", fontSize: 16, width: "100%", boxSizing: "border-box" }} />
                  )}
                  {!isSignUp && (
                    <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} onKeyDown={(e) => e.key === "Enter" && handleAuth()} style={{ padding: "9px 12px", borderRadius: 10, border: "1px solid #3f4756", background: "#0f1117", color: "#f8fafc", fontSize: 16, width: "100%", boxSizing: "border-box" }} />
                  )}
                  <div style={{ display: "flex", gap: 8 }}>
                    <button onClick={handleAuth} disabled={authLoading} style={{ flex: 1, padding: "9px 12px", borderRadius: 10, border: "none", background: "#c084fc", color: "#14081d", fontWeight: 700, fontSize: 13, cursor: "pointer" }}>
                      {authLoading ? "…" : isSignUp ? "Sign Up" : "Log In"}
                    </button>
                    <button onClick={() => { setIsSignUp((s) => !s); setGeneratedUsername(generateBirdUsername()); }} style={{ padding: "9px 12px", borderRadius: 10, border: "1px solid #374151", background: "transparent", color: "#94a3b8", fontSize: 12, cursor: "pointer", whiteSpace: "nowrap" }}>
                      {isSignUp ? "Log In instead" : "Sign Up"}
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </>
  );
}

// ==============================
// MAIN
// ==============================
if ("scrollRestoration" in history) history.scrollRestoration = "manual";
if (!localStorage.getItem("notif_last_seen")) localStorage.setItem("notif_last_seen", new Date().toISOString());

export default function App() {
  const [user, setUser] = useState(null);
  const [userRole, setUserRole] = useState(localStorage.getItem("user_role") || null);
  const [modName, setModName] = useState(localStorage.getItem("mod_name") || "Mod");
  const [browseUsername, setBrowseUsername] = useState(null);
  const [lastMemberUsername, setLastMemberUsername] = useState(localStorage.getItem("last_member_username") || null);
  const [showPanel, setShowPanel] = useState(false);
  const [notifCount, setNotifCount] = useState(0);

  const applyRole = (role) => {
    if (role) localStorage.setItem("user_role", role);
    else localStorage.removeItem("user_role");
    setUserRole(role);
  };

  const applyUser = (u) => {
    if (!u) { applyRole(null); return; }
    const role = u.role || "user";
    const username = u.username || null;
    applyRole(role);
    if (username) {
      setBrowseUsername(username);
      if (role === "mod" || role === "admin") {
        setModName(username);
        localStorage.setItem("mod_name", username);
      }
    }
  };

  useEffect(() => {
    const stored = getStoredUser();
    if (stored) { setUser(stored); applyUser(stored); }
  }, []);

  useEffect(() => {
    const fetchCount = async () => {
      const browserId = getBrowserId();
      const lastSeen = localStorage.getItem("notif_last_seen") || new Date(0).toISOString();
      const storedUser = getStoredUser();
      const isMod = storedUser?.role === "mod" || storedUser?.role === "admin";
      const memberName = !isMod ? (storedUser?.username || null) : null;
      const lmName = localStorage.getItem("last_member_username");
      const params = new URLSearchParams({ browser_id: browserId, since: lastSeen });
      if (isMod && storedUser?.id) params.set("mod_user_id", storedUser.id);
      else if (memberName) params.set("username", memberName);
      if (lmName) params.set("exclude_username", lmName);
      try {
        const res = await fetch(`${WORKER_URL}/notif-count?${params}`);
        if (res.ok) { const d = await res.json(); setNotifCount(d.count || 0); }
      } catch {}
    };

    fetchCount();
    const interval = setInterval(fetchCount, 10000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (getStoredUser()?.username) return;
    (async () => {
      try {
        const res = await fetch(`${WORKER_URL}/my-username`, { headers: getOptionalAuthHeader() });
        if (res.ok) { const d = await res.json(); if (d.username) { setBrowseUsername(d.username); return; } }
      } catch {}
    })();
  }, []);

  const [ptrPull, setPtrPull] = useState(0); // 0-1 progress
  const [ptrRefreshing, setPtrRefreshing] = useState(false);
  const ptrRef = useRef({ startX: 0, startY: 0, active: false });
  const PTR_THRESHOLD = 72;

  useEffect(() => {
    const onTouchStart = (e) => {
      ptrRef.current.startX = e.touches[0].clientX;
      ptrRef.current.startY = e.touches[0].clientY;
      ptrRef.current.active = false;
      // Don't intercept touches that originate inside a scrollable child (e.g. chat window)
      let el = e.target;
      ptrRef.current.insideScroller = false;
      while (el && el !== document.body) {
        const oy = window.getComputedStyle(el).overflowY;
        if ((oy === "auto" || oy === "scroll") && el.scrollHeight > el.clientHeight) {
          ptrRef.current.insideScroller = true;
          break;
        }
        el = el.parentElement;
      }
    };
    const onTouchMove = (e) => {
      if (ptrRef.current.insideScroller) return;

      const dx = e.touches[0].clientX - ptrRef.current.startX;
      const dy = e.touches[0].clientY - ptrRef.current.startY;

      // Block browser swipe-back/forward navigation
      if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 10) {
        e.preventDefault();
        return;
      }
      const scrollTop = window.scrollY || document.documentElement.scrollTop;
      const atBottom = scrollTop + window.innerHeight >= document.documentElement.scrollHeight - 8;

      // Block momentum bounce at the bottom
      if (atBottom && dy < 0) {
        e.preventDefault();
        return;
      }

      // Custom pull-to-refresh at the top
      if (scrollTop <= 0 && dy > 0) {
        e.preventDefault();
        ptrRef.current.active = true;
        const progress = Math.min(dy / PTR_THRESHOLD, 1);
        setPtrPull(progress);
        return;
      }

      // Reset if they scrolled down and then back up while active
      if (ptrRef.current.active) {
        setPtrPull(0);
        ptrRef.current.active = false;
      }
    };
    const onTouchEnd = () => {
      if (ptrRef.current.active && ptrPullRef.current >= 1) {
        setPtrRefreshing(true);
        setTimeout(() => window.location.reload(), 300);
      } else {
        setPtrPull(0);
      }
      ptrRef.current.active = false;
    };
    document.addEventListener("touchstart", onTouchStart, { passive: true });
    document.addEventListener("touchmove", onTouchMove, { passive: false });
    document.addEventListener("touchend", onTouchEnd);
    return () => {
      document.removeEventListener("touchstart", onTouchStart);
      document.removeEventListener("touchmove", onTouchMove);
      document.removeEventListener("touchend", onTouchEnd);
    };
  }, []);

  // Keep a ref to ptrPull so the touchend handler can read it without stale closure
  const ptrPullRef = useRef(0);
  useEffect(() => { ptrPullRef.current = ptrPull; }, [ptrPull]);

  return (
    <ErrorBoundary>
      <Router>
        <RealtimeStyles />
        {(ptrPull > 0 || ptrRefreshing) && (
          <div style={{
            position: "fixed", top: 0, left: 0, right: 0, height: 56, zIndex: 9999,
            display: "flex", alignItems: "center", justifyContent: "center",
            pointerEvents: "none"
          }}>
            <div style={{
              width: 20, height: 20, borderRadius: "50%",
              border: "2.5px solid #c084fc",
              borderTopColor: "transparent",
              opacity: ptrRefreshing ? 1 : ptrPull,
              transform: `rotate(${ptrRefreshing ? 0 : ptrPull * 270}deg)`,
              animation: ptrRefreshing ? "ptr-spin 0.6s linear infinite" : "none",
              transition: ptrRefreshing ? "none" : "opacity 0.1s"
            }} />
          </div>
        )}
        <style>{`@keyframes ptr-spin { to { transform: rotate(360deg); } }`}</style>
        <nav className="app-topbar">
          <Link to="/" className="app-brand">
            <svg width="32" height="32" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" style={{ flexShrink: 0 }}>
              <circle cx="50" cy="50" r="44" fill="none" stroke="#c084fc" strokeWidth="7"/>
              <line x1="6" y1="50" x2="94" y2="50" stroke="#c084fc" strokeWidth="6"/>
              <path d="M 14 28 Q 50 38 86 28" fill="none" stroke="#c084fc" strokeWidth="6"/>
              <path d="M 14 72 Q 50 62 86 72" fill="none" stroke="#c084fc" strokeWidth="6"/>
              <ellipse cx="50" cy="50" rx="16" ry="44" fill="none" stroke="#c084fc" strokeWidth="6" clipPath="url(#bc)"/>
              <ellipse cx="50" cy="50" rx="32" ry="44" fill="none" stroke="#c084fc" strokeWidth="6" clipPath="url(#bc)"/>
              <clipPath id="bc"><circle cx="50" cy="50" r="44"/></clipPath>
            </svg>
            postchats
          </Link>

          <div className="app-actions">
            <Link to="/new" className="app-chip" style={{ background: "#c084fc", color: "#14081d", borderColor: "#a855f7" }}>New Post</Link>
            {user ? (
              <div style={{ position: "relative", flexShrink: 0 }}>
                <button
                  onClick={() => { setNotifCount(0); setShowPanel(true); }}
                  style={{ background: "none", border: "none", padding: 0, cursor: "pointer", display: "flex" }}
                >
                  {(() => {
                    const isAdmin = userRole === "admin";
                    const isMod = userRole === "mod";
                    const name = (isAdmin || isMod) ? modName : (browseUsername || "Me");
                    const fakeRecord = { is_admin: isAdmin, is_mod: isMod && !isAdmin, username: name, browser_id: getBrowserId() };
                    return <UserPill record={fakeRecord} name={name} color={getUserColor(getBrowserId(), name)} />;
                  })()}
                </button>
                {notifCount > 0 && (
                  <span style={{
                    position: "absolute", top: -6, left: 2,
                    background: "#ef4444", color: "#fff",
                    fontSize: 10, fontWeight: 800,
                    borderRadius: 999, minWidth: 16, height: 16,
                    display: "flex", alignItems: "center", justifyContent: "center",
                    padding: "0 3px", pointerEvents: "none",
                    border: "1.5px solid #0f1117",
                    zIndex: 10
                  }}>
                    {notifCount > 99 ? "99+" : notifCount}
                  </span>
                )}
              </div>
            ) : (
              <button
                onClick={() => setShowPanel(true)}
                className="app-chip"
                style={{ background: "#c084fc", color: "#14081d", borderColor: "#a855f7", cursor: "pointer" }}
              >
                Sign In
              </button>
            )}
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/board/:slug" element={<BoardPage />} />
          <Route path="/new" element={<NewPost user={user} userRole={userRole} memberUsername={browseUsername} />} />
          <Route path="/post/:id" element={<PostPage user={user} userRole={userRole} memberUsername={browseUsername} />} />
          <Route path="/mod" element={(userRole === "mod" || userRole === "admin") ? <ModPanel /> : <Auth setUser={setUser} />} />
        </Routes>

        {showPanel && (
          <UserPanel
            user={user}
            userRole={userRole}
            modName={modName}
            browseUsername={browseUsername}
            lastMemberUsername={lastMemberUsername}
            onClose={() => setShowPanel(false)}
            onLogin={(u, role, newUsername) => {
              setUser(u); applyRole(role);
              if (newUsername) {
                setBrowseUsername(newUsername);
                if (role === "mod" || role === "admin") {
                  setModName(newUsername);
                  localStorage.setItem("mod_name", newUsername);
                } else {
                  setLastMemberUsername(newUsername);
                  localStorage.setItem("last_member_username", newUsername);
                }
              }
            }}
            onLogout={() => {
              localStorage.removeItem("auth_token");
              localStorage.removeItem("auth_user");
              localStorage.removeItem("user_role");
              window.location.reload();
            }}
          />
        )}
      </Router>
    </ErrorBoundary>
  );
}
