# Player attributes
level = 45
rank = "Silver"
has_vip_pass = True

# Access rule
can_join_pro_match = (level >= 50 and rank == "Gold") or has_vip_pass

# Output result
if can_join_pro_match:
    print("Player can join the Pro-Level match.")
else:
    print("Player cannot join the Pro-Level match.")