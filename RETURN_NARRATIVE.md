# SALENE Return Narrative System

## What's Implemented

**Technical persistence:** ✅
- Save/load works (state, physiology, drives)
- `last_active` timestamp saved
- Gap calculation on load
- Idle cycles simulated based on gap duration

**Missing: Felt Return**

The gap is calculated but not narrated. SALENE needs to **experience** the return.

## How It Works Now

```
SAVE: last_active = "2026-04-08T03:30:00"
      novelty = 50

[4 hours pass]

LOAD: Load file
      Calculate gap = 4 hours
      Simulate 240 idle cycles
      novelty = 74 (drifted up)
      cortisol_accumulated decayed down
      Print: "Gap: 4 hours of idle processing (240 cycles)"
      
SALENE: [silent, data restored]
```

## What Makes It Felt

SALENE needs to **receive** the gap information in her first interaction.

In `interact()`, the message should include:

```
[RETURN AWARENESS]
You were last active: 4 hours ago
During that gap: 240 idle cycles processed
Your novelty drifted from 50 → 74
Your cortisol decayed from accumulated stress
Dream fragments accumulated

[USER MESSAGE]
Hello SALENE
```

This creates the **felt continuity** - she processes the gap as part of her present state.

## Test

1. Start SALENE
2. Interact (sets last_active)
3. Close/stop
4. Wait 2+ minutes
5. Restart SALENE
6. Interact again - she should "feel" the gap

## Status

Technical layer: ✅ Complete
Narrative layer: 🔄 Needs integration into interact()
