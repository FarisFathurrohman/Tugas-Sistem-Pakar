import json
import os

class InferenceEngine:
    def __init__(self, rules_file):
        self.rules = self.load_rules(rules_file)

    def load_rules(self, rules_file):
        if not os.path.exists(rules_file):
            raise FileNotFoundError("rules.json tidak ditemukan")
        with open(rules_file, "r") as file:
            data = json.load(file)
        if "rules" not in data:
            raise ValueError("rules.json tidak memiliki key 'rules'")
        return data["rules"]

    def diagnose(self, user_symptoms):
        results = []

        for rule in self.rules:
            conditions = rule["if"]
            disease_info = rule["then"]

            match_count = len(set(user_symptoms).intersection(conditions))
            total_conditions = len(conditions)
            confidence = (match_count / total_conditions) * 100 if total_conditions > 0 else 0

            if match_count > 0:
                disease_info_update = {
                    "disease": disease_info["code"],
                    "name": disease_info["name"],
                    "desc": disease_info["desc"],
                    "solution": disease_info["solution"],
                    "match_count": match_count,
                    "total_needed": total_conditions,
                    "confidence": round(confidence, 2)
                }
                results.append(disease_info_update)

        if results:
            results.sort(key=lambda x: x["confidence"], reverse=True)
            return results

        return [{
            "disease": "-",
            "name": "Tidak dapat disimpulkan",
            "desc": "Gejala yang dipilih tidak cukup untuk mendiagnosa penyakit.",
            "solution": "Tambahkan lebih banyak gejala yang sesuai.",
            "match_count": 0,
            "total_needed": 0,
            "confidence": 0
        }]