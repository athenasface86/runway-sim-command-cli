import argparse
import json


def months_of_runway(cash: float, monthly_burn: float) -> float:
    if cash < 0:
        raise ValueError("cash must be non-negative.")
    if monthly_burn <= 0:
        raise ValueError("monthly_burn must be greater than zero.")
    return cash / monthly_burn


def simulate(cash: float, burn: float, revenue: float = 0, growth: float = 0, months: int = 12) -> list[dict]:
    if months < 1 or months > 60:
        raise ValueError("months must be between 1 and 60.")
    if burn <= 0:
        raise ValueError("burn must be greater than zero.")
    if cash < 0 or revenue < 0:
        raise ValueError("cash and revenue must be non-negative.")

    rows = []
    balance = cash
    current_revenue = revenue
    for month in range(1, months + 1):
        net_burn = max(burn - current_revenue, 0)
        balance -= net_burn
        rows.append(
            {
                "month": month,
                "revenue": round(current_revenue, 2),
                "net_burn": round(net_burn, 2),
                "ending_cash": round(balance, 2),
                "runway_remaining": round(months_of_runway(max(balance, 0), burn), 2),
            }
        )
        current_revenue *= 1 + growth
    return rows


def scenario_pack(cash: float, burn: float, revenue: float) -> dict:
    scenarios = {
        "base": {"burn": burn, "growth": 0.04},
        "lean": {"burn": burn * 0.82, "growth": 0.03},
        "growth": {"burn": burn * 1.18, "growth": 0.08},
    }
    return {
        name: simulate(cash, values["burn"], revenue, values["growth"], months=12)
        for name, values in scenarios.items()
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Model startup runway and monthly cash scenarios.")
    parser.add_argument("--cash", type=float, required=True, help="Starting cash balance.")
    parser.add_argument("--burn", type=float, required=True, help="Monthly operating burn.")
    parser.add_argument("--revenue", type=float, default=0, help="Current monthly revenue.")
    parser.add_argument("--months", type=int, default=12, help="Months to simulate.")
    parser.add_argument("--growth", type=float, default=0.04, help="Monthly revenue growth rate.")
    parser.add_argument("--pack", action="store_true", help="Print base, lean, and growth scenarios.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    payload = (
        scenario_pack(args.cash, args.burn, args.revenue)
        if args.pack
        else simulate(args.cash, args.burn, args.revenue, args.growth, args.months)
    )
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
