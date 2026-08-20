import React from 'react';
import { getIconComponent } from '../utils/themeMap';

export const SCENARIOS = [
  { id: 'sully', name: 'RH & Emploi', prompt: 'Affiche la vacance des postes hospitaliers (+6 mois)' },
  { id: 'credit_advisor', name: 'Risque Crédit', prompt: 'Analyse le scoring de faillite IFRS 9 pour ce trimestre' },
  { id: 'net_arch', name: 'Télécoms 5G', prompt: 'Fais un diagnostic de la QoS réseau sur la zone Sud-Ouest' },
  { id: 'earth_intel', name: 'Spatial & Sat', prompt: "Calcule l'indice de santé chlorophyllienne NDVI du secteur" },
  { id: 'transit_navigator', name: 'Transports', prompt: 'Quelles sont les lignes SNCF ayant subi le plus de retards aujourd\'hui ?' },
  { id: 'pulse_checker', name: 'Santé Publique', prompt: 'Affiche le taux de rupture des stocks de médicaments critiques' },
  { id: 'shelf_optimizer', name: 'CPG Retail', prompt: 'Génère la liste des produits en rupture en rayon Frais à 14 jours' },
  { id: 'arena_manager', name: 'Sport & Stades', prompt: 'Analyse le panier moyen des spectateurs en loge VIP' },
  { id: 'helios', name: 'Énergie IRVE', prompt: 'Quelles sont les bornes de recharge IRVE surchargées ?' },
  { id: 'ceres', name: 'Agriculture', prompt: "Quel est le bilan carbone ACV ADEME pour l'exploitation ?" },
  { id: 'cine_analyst', name: 'Box-Office', prompt: 'Calcule la part de marché des cinémas par format immersif' }
];

export function ScenarioChips({ agents, selectedAgent, onSelectAgent, onSendMessage }) {
  return (
    <div className="w-full flex items-center justify-center py-1">
      <div className="extension-chips-container max-w-full" id="scenariosContainer">
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
              className={`chip ${isSelected ? 'active' : ''}`}
            >
              <div className="img-container">
                <IconComp className="w-3.5 h-3.5" />
              </div>
              <span className="chip-text">{sc.name}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
