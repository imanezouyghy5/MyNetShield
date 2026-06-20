# main.py - MyNetShield : Intégration complète IA + détection d'anomalies (Jalon 3)
import logging
from pathlib import Path
import json
from datetime import datetime
import os

# Composants ML (exigés Semaine 6 – Plan de Projet)
from app.ml.data_preprocessor import DataPreprocessor
from app.ml.ml_anomaly import MLAnomalyDetector
from app.ml.model_trainer import ModelTrainer

# Scanner enrichi (conforme Diagramme de Séquence II)
from app.scanner.network_scanner import NetworkScanner

# Configuration des logs
logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger("MyNetShield")


def _load_snapshots(snapshot_dir: Path) -> list:
    """Charge tous les snapshots sauvegardés (Privacy by Design – Cahier §IV.1)"""
    if not snapshot_dir.exists():
        return []
    return [
        json.load(open(f, "r", encoding="utf-8"))
        for f in sorted(snapshot_dir.glob("scan_*.json"))
        if f.is_file()
    ]


def _train_model(trainer: ModelTrainer, snapshot_dir: Path) -> bool:
    """Entraîne le modèle sur l'historique des scans (conforme Plan Semaine 6)"""
    devices_history = _load_snapshots(snapshot_dir)

    if not devices_history:
        print("❌ Aucun snapshot trouvé. Effectuez d'abord 2-3 scans réseau.")
        return False

    total_devices = sum(len(snapshot) for snapshot in devices_history)
    if total_devices < 5:
        print(
            f"⚠️  Pas assez de données (minimum 5 appareils requis, actuellement {total_devices})."
        )
        print("💡 Effectuez plus de scans pour collecter des données.")
        return False

    print(
        f"\n🧠 Entraînement du modèle sur {len(devices_history)} snapshots ({total_devices} appareils)..."
    )
    print(
        "   (Isolation Forest – détection non supervisée conforme État de l'Art III.3)"
    )

    try:
        result = trainer.train_on_historical_data(devices_history)
        if result.get("success"):
            record = result["record"]
            print("\n✅ MODÈLE ENTRAÎNÉ AVEC SUCCÈS !")
            print(f"   📊 Échantillons utilisés : {record['samples']}")
            print(f"   📊 Snapshots combinés : {record['snapshots']}")
            print(f"   📊 Features analysés : {record['features']}")
            print(f"   📊 Seuil d'anomalies : {record['contamination']:.0%}")
            print(
                f"\n💡 Le modèle est prêt ! Relancez un scan pour détecter les anomalies."
            )
            return True
        else:
            print(
                f"\n❌ Échec de l'entraînement : {result.get('message', 'Erreur inconnue')}"
            )
            return False
    except Exception as e:
        print(f"\n❌ Erreur critique lors de l'entraînement : {e}")
        return False


def _scan_network(
    scanner: NetworkScanner, preprocessor: DataPreprocessor, detector: MLAnomalyDetector
):
    """Scan réseau + détection d'anomalies si modèle entraîné (conforme Cahier §II.3)"""
    print("\n🔍 Scan du réseau en cours (ARP + identification + ports)...")
    scan_result = scanner.scan_full()
    devices = [d for d in scan_result["devices"] if d["status"] == "online"]

    if not devices:
        print("❌ Aucun appareil en ligne détecté.")
        return

    print(f"✅ {len(devices)} appareils en ligne identifiés.\n")

    # Cas 1 : Modèle NON entraîné → sauvegarde pour entraînement futur
    if not detector.is_trained:
        print("⚠️  MODÈLE D'IA NON ENTRAÎNÉ")
        print("💡 Conseil (Cahier §II.3) :")
        print("   1. Effectuez 2-3 scans supplémentaires")
        print("   2. Sélectionnez 'Entraîner le modèle' dans le menu")
        print("   3. Relancez un scan pour activer la détection d'anomalies\n")

        snapshot_dir = Path("data/training_snapshots")
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        snapshot_file = (
            snapshot_dir / f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        ml_ready = [
            {
                "ip": d["ip"],
                "mac": d["mac"],
                "hostname": d["hostname"],
                "device_type": d["device_type"],
                "open_ports": d["open_ports"],
                "vulnerabilities": d["vulnerabilities"],
                "traffic_history": d["traffic_history"],
            }
            for d in devices
        ]

        with open(snapshot_file, "w", encoding="utf-8") as f:
            json.dump(ml_ready, f, indent=2, ensure_ascii=False)
        print(f"💾 Scan sauvegardé pour entraînement : {snapshot_file}")
        return

    # Cas 2 : Modèle ENTRAÎNÉ → détection d'anomalies
    print("🧠 Analyse comportementale par IA locale (Isolation Forest)...")
    try:
        enriched = detector.detect_anomalies(devices, preprocessor)
    except RuntimeError as e:
        print(f"❌ Erreur : {e}")
        return

    anomalies = [d for d in enriched if d.get("ml_anomaly_detected")]
    print(f"\n🎯 RÉSULTAT : {len(anomalies)}/{len(enriched)} appareils suspects\n")

    if anomalies:
        print("=" * 70)
        print("🚨 APPAREILS SUSPECTS DÉTECTÉS (Conforme Cahier §II.3)")
        print("=" * 70)
        for dev in anomalies:
            print(
                f"\n📍 {dev['ip']} | {dev.get('hostname', 'Inconnu')} ({dev.get('device_type', 'Appareil')})"
            )
            print(
                f"   🔒 Niveau de risque : {dev.get('ml_risk_level', 'inconnu').upper()}"
            )
            print(
                f"   💡 Explication : {dev.get('ml_anomaly_reason', 'Activité anormale détectée')}"
            )
        print(
            "\nℹ️  Pour plus de détails, utilisez l'IA conversationnelle (Semaine 5) :"
        )
        print("    « Pourquoi cette caméra communique-t-elle la nuit ? »")
    else:
        print("✅ Aucune activité suspecte détectée. Votre réseau est sécurisé !")
        print("💡 Recommandation ANRT 2025 : Effectuez un scan hebdomadaire.")


def main():
    print("🛡️  MYNETSHIELD – Plateforme Locale de Sécurité Réseau")
    print("=" * 65)
    print("✅ Conforme Cahier des Charges §IV.1 : AUCUNE DONNÉE NE QUITTE VOTRE RÉSEAU")
    print("✅ Conforme Plan de Projet Semaine 6 : Application complète avec IA active")
    print("=" * 65)

    # Initialisation des composants (100% local – Cahier §III.2)
    scanner = NetworkScanner()
    preprocessor = DataPreprocessor()
    detector = MLAnomalyDetector()
    trainer = ModelTrainer(detector, preprocessor)
    snapshot_dir = Path("data/training_snapshots")

    # Menu principal (interface utilisateur non-technicien – Cahier §II.3)
    while True:
        print("\n" + "=" * 65)
        print("MENU PRINCIPAL")
        print("=" * 65)
        print(
            f"[1] 🔍 Scanner le réseau {'(MODÈLE PRÊT ✅)' if detector.is_trained else '(MODÈLE NON ENTRAÎNÉ ⚠️)'}"
        )
        print(
            f"[2] 🧠 Entraîner le modèle {'(Snapshots: ' + str(len(list(snapshot_dir.glob('scan_*.json')))) + ')' if snapshot_dir.exists() else '(Aucun snapshot)'}"
        )
        print("[3] 👋 Quitter")
        print("=" * 65)

        choix = input("\nSélectionnez une option (1-3) : ").strip()

        if choix == "1":
            _scan_network(scanner, preprocessor, detector)
        elif choix == "2":
            _train_model(trainer, snapshot_dir)
        elif choix == "3":
            print("\n👋 Au revoir ! Votre réseau reste sécurisé localement.")
            break
        else:
            print("❌ Option invalide. Veuillez choisir 1, 2 ou 3.")

        input("\nAppuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    main()
