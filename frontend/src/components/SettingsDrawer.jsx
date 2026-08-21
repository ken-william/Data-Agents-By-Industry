import React from 'react';
import { X, Volume2, VolumeX, Monitor, Palette, Sparkles } from 'lucide-react';
import { cn } from '../utils/cn';

export const THEMES = [
  { id: 'cloud-next', name: 'Google Cloud Next', desc: 'Officiel : Bleu #4285F4, Rouge, Jaune & Vert', colorPreview: 'from-[#4285F4] via-[#EA4335] to-[#34A853]' },
  { id: 'gemini-aurora', name: 'Gemini Aurora', desc: 'Événementiel : Cyan, Violet & Rose Corail', colorPreview: 'from-[#38BDF8] via-[#C084FC] to-[#EC4899]' },
  { id: 'tech-sunset', name: 'Techmakers Sunset', desc: 'Ambiance Chaleureuse : Magenta, Orange & Or', colorPreview: 'from-[#E11D48] via-[#F97316] to-[#F59E0B]' },
  { id: 'eco-system', name: 'Workspace Harmony', desc: 'Signature Durable : Émeraude, Menthe & Teal', colorPreview: 'from-[#10B981] via-[#34D399] to-[#06B6D4]' }
];

export function SettingsDrawer({
  isOpen,
  onClose,
  autoSpeechEnabled,
  setAutoSpeechEnabled,
  screenMode,
  setScreenMode,
  activeTheme,
  setActiveTheme,
  selectedAgent,
  agentsCount
}) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/60 backdrop-blur-md animate-fade-in">
      
      {/* Drawer Panel */}
      <div className="w-full max-w-md bg-slate-900 border-l border-slate-800 h-full p-6 flex flex-col justify-between overflow-y-auto text-slate-100 shadow-2xl">
        
        <div className="space-y-6">
          
          {/* Header */}
          <div className="flex items-center justify-between pb-4 border-b border-slate-800">
            <div className="flex items-center gap-2">
              <Sparkles className="size-5 text-sky-400" />
              <h3 className="text-base font-bold text-white font-['Google_Sans_Flex']">
                Paramètres & Thèmes Événementiels
              </h3>
            </div>
            <button
              type="button"
              onClick={onClose}
              className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition-colors"
            >
              <X className="size-5" />
            </button>
          </div>

          {/* Theme Selector Section */}
          <div className="space-y-3">
            <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-400">
              <Palette className="size-4 text-sky-400" />
              <span>Thèmes Visuels Événementiels</span>
            </div>

            <div className="grid grid-cols-1 gap-2.5">
              {THEMES.map((t) => {
                const isSelected = activeTheme === t.id;

                return (
                  <button
                    key={t.id}
                    type="button"
                    onClick={() => setActiveTheme(t.id)}
                    className={cn(
                      "p-3.5 rounded-2xl border text-left transition-all flex items-center justify-between gap-3",
                      isSelected
                        ? "bg-slate-800 border-sky-400 shadow-md"
                        : "bg-slate-950/60 border-slate-800 hover:border-slate-700 hover:bg-slate-800/50 text-slate-300"
                    )}
                  >
                    <div>
                      <div className="flex items-center gap-2">
                        <span className={cn("size-3 rounded-full bg-gradient-to-r shrink-0", t.colorPreview)} />
                        <span className="text-xs font-bold text-white">{t.name}</span>
                      </div>
                      <span className="text-[11px] text-slate-400 block mt-0.5">{t.desc}</span>
                    </div>

                    {isSelected && (
                      <span className="text-[10px] px-2 py-0.5 rounded-full bg-sky-500/20 text-sky-300 border border-sky-400/40 font-bold shrink-0">
                        • Actif
                      </span>
                    )}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Screen Mode Section */}
          <div className="space-y-3 pt-2 border-t border-slate-800">
            <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-400">
              <Monitor className="size-4 text-sky-400" />
              <span>Mode d'Affichage Double Écran</span>
            </div>

            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() => setScreenMode('showcase')}
                className={cn(
                  "p-3 rounded-xl border text-xs font-semibold text-center transition-all",
                  screenMode === 'showcase'
                    ? "bg-sky-500/20 border-sky-400 text-sky-300 shadow-sm"
                    : "bg-slate-950/60 border-slate-800 text-slate-400 hover:text-slate-200"
                )}
              >
                Écran A : Showcase
              </button>

              <button
                type="button"
                onClick={() => setScreenMode('controller')}
                className={cn(
                  "p-3 rounded-xl border text-xs font-semibold text-center transition-all",
                  screenMode === 'controller'
                    ? "bg-sky-500/20 border-sky-400 text-sky-300 shadow-sm"
                    : "bg-slate-950/60 border-slate-800 text-slate-400 hover:text-slate-200"
                )}
              >
                Écran B : Contrôleur
              </button>
            </div>
          </div>

          {/* Voice Output Toggle */}
          <div className="space-y-3 pt-2 border-t border-slate-800">
            <div className="flex items-center justify-between p-3.5 rounded-2xl bg-slate-950/60 border border-slate-800">
              <div className="flex items-center gap-3">
                {autoSpeechEnabled ? <Volume2 className="size-5 text-emerald-400" /> : <VolumeX className="size-5 text-slate-500" />}
                <div>
                  <span className="text-xs font-bold text-white block">Synthèse Vocale Live</span>
                  <span className="text-[11px] text-slate-400">Lecture orale automatique des réponses</span>
                </div>
              </div>

              <input
                type="checkbox"
                checked={autoSpeechEnabled}
                onChange={(e) => setAutoSpeechEnabled(e.target.checked)}
                className="size-5 rounded border-slate-700 text-sky-500 focus:ring-sky-400 cursor-pointer"
              />
            </div>
          </div>

        </div>

        {/* Footer Info */}
        <div className="pt-4 border-t border-slate-800 text-center text-[11px] text-slate-500">
          <p>Talk to Data • Google Luminous Aurora Engine</p>
        </div>

      </div>

    </div>
  );
}
