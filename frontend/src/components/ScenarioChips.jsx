import React, { useRef } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { getIconComponent } from '../utils/themeMap';
import { cn } from '../utils/cn';

export const SCENARIOS = [
  { id: 'sully', name: 'RH & Emploi Public', prompt: 'Affiche la vacance des postes hospitaliers (+6 mois)' },
  { id: 'credit_advisor', name: 'Risque Crédit & Finance', prompt: 'Analyse le scoring de faillite IFRS 9 pour ce trimestre' },
  { id: 'net_arch', name: 'Télécoms & Réseau 5G', prompt: 'Fais un diagnostic de la QoS réseau sur la zone Sud-Ouest' },
  { id: 'earth_intel', name: 'Spatial & Satellite', prompt: "Calcule l'indice de santé chlorophyllienne NDVI du secteur" },
  { id: 'transit_navigator', name: 'Transports & SNCF', prompt: 'Quelles sont les lignes SNCF ayant subi le plus de retards aujourd\'hui ?' },
  { id: 'pulse_checker', name: 'Santé Publique', prompt: 'Affiche le taux de rupture des stocks de médicaments critiques' },
  { id: 'shelf_optimizer', name: 'CPG & Grande Distribution', prompt: 'Génère la liste des produits en rupture en rayon Frais à 14 jours' },
  { id: 'arena_manager', name: 'Sport, Stades & VIP', prompt: 'Analyse le panier moyen des spectateurs en loge VIP' },
  { id: 'helios', name: 'Énergie & Bornes IRVE', prompt: 'Quelles sont les bornes de recharge IRVE surchargées ?' },
  { id: 'ceres', name: 'Agriculture & Bilan Carbone', prompt: "Quel est le bilan carbone ACV ADEME pour l'exploitation ?" },
  { id: 'cine_analyst', name: 'Box-Office & Cinéma', prompt: 'Calcule la part de marché des cinémas par format immersif' }
];

export function ScenarioChips({ agents, selectedAgent, onSelectAgent, onSendMessage }) {
  const containerRef = useRef(null);

  const scroll = (direction) => {
    if (containerRef.current) {
      const amount = direction === 'left' ? -280 : 280;
      containerRef.current.scrollBy({ left: amount, behavior: 'smooth' });
    }
  };

  return (
    <div className="w-full flex items-center justify-center gap-2 py-1 max-w-full mx-auto relative group">
      
      {/* Scroll Left Button */}
      <button
        type="button"
        aria-label="Défiler les puces vers la gauche"
        onClick={() => scroll('left')}
        className="size-8 rounded-full bg-white hover:bg-slate-100 border border-slate-200 text-slate-700 transition-all shadow-2xs shrink-0 flex items-center justify-center hover:scale-105 active:scale-95"
        title="Défiler vers la gauche"
      >
        <ChevronLeft className="size-4" />
      </button>

      {/* Extension Chips Scrollable Container */}
      <div
        ref={containerRef}
        className="extension-chips-container max-w-full scroll-smooth flex items-center gap-2.5 py-1"
        id="scenariosContainer"
      >
        {SCENARIOS.map((sc) => {
          const isSelected = selectedAgent?.id === sc.id;
          const IconComp = getIconComponent(sc.id);
          const targetAgent = agents.find(a => a.id === sc.id) || selectedAgent;

          return (
            <div
              key={sc.id}
              onClick={() => {
                if (targetAgent) {
                  onSelectAgent(targetAgent);
                }
                if (onSendMessage) {
                  onSendMessage(sc.prompt);
                }
              }}
              className={cn("awwwards-pill", isSelected && "active")}
            >
              <IconComp className={cn("size-4 shrink-0", isSelected ? "text-white" : "text-[#0B57D0]")} />
              <span>{sc.name}</span>
            </div>
          );
        })}
      </div>

      {/* Scroll Right Button */}
      <button
        type="button"
        aria-label="Défiler les puces vers la droite"
        onClick={() => scroll('right')}
        className="size-8 rounded-full bg-white hover:bg-slate-100 border border-slate-200 text-slate-700 transition-all shadow-2xs shrink-0 flex items-center justify-center hover:scale-105 active:scale-95"
        title="Défiler vers la droite"
      >
        <ChevronRight className="size-4" />
      </button>

    </div>
  );
}
