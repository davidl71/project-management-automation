# Task Status Workflow Discipline

**Status**: Active Guidelines  
**Last Updated**: 2025-12-25

---

## 🎯 Core Principle

**Task status should reflect actual work state, not just intent.**

Time tracking only counts when tasks are actively "In Progress". Idle time must not inflate actual work hours.

---

## 📋 Status Definitions

### **Todo**
- **When**: Task is planned but not yet started
- **Action**: Default status for new tasks
- **Time Tracking**: No time counted

### **In Progress**
- **When**: Actively working on the task RIGHT NOW
- **Action**: Only set when you're actively working
- **Time Tracking**: Time counted only during active work
- **⚠️ Critical**: Move back to "Todo" when stopping work (even temporarily)

### **Review**
- **When**: Work is complete, awaiting approval/feedback
- **Action**: Set when ready for human review
- **Time Tracking**: Work time complete, awaiting review time

### **Done**
- **When**: Task is fully complete and approved
- **Action**: Final status after review approval
- **Time Tracking**: Final actual hours recorded

---

## ⚠️ Common Mistakes to Avoid

### ❌ **DO NOT:**
1. Leave tasks "In Progress" when switching to other work
2. Leave tasks "In Progress" overnight or during breaks
3. Leave tasks "In Progress" while waiting for dependencies
4. Calculate time from task creation to completion (includes idle time)

### ✅ **DO:**
1. Move to "In Progress" ONLY when actively working
2. Move back to "Todo" when stopping work (even for a few minutes)
3. Use "In Progress" as a "currently working on this" indicator
4. Record actual work time separately from elapsed time

---

## 🔄 Daily Workflow

### Starting Work
```
1. Select task from "Todo"
2. Change status to "In Progress"
3. Begin work
```

### Stopping Work
```
1. Save your progress
2. Change status back to "Todo"
3. Resume later from "Todo"
```

### Completing Work
```
1. Finish implementation
2. Change status to "Review"
3. Add result comment
4. Wait for approval
5. Change to "Done" after approval
```

---

## ⏱️ Time Tracking Best Practices

### Active Work Time vs. Elapsed Time

**Problem**: Tasks staying "In Progress" for days accumulate massive "time spent" values that don't reflect actual work.

**Solution**: 
- Only count time when task is actively "In Progress"
- Track work sessions separately
- Record actual work hours in `actualHours` field when completing tasks

### Example

**Bad**: 
- Task created: Dec 1
- Status: "In Progress" (left idle)
- Last modified: Dec 25
- Calculated time: 576 hours ❌ (wrong!)

**Good**:
- Task created: Dec 1
- Work sessions: Dec 1 (2h), Dec 5 (3h), Dec 10 (1h)
- Actual work: 6 hours ✅ (correct!)

---

## 🤖 Automation Support

### Stale Task Detection

The system automatically detects tasks that are "In Progress" but haven't been updated recently:

- **Threshold**: 2 hours of inactivity
- **Action**: Auto-move back to "Todo" status
- **Runs**: Part of daily automation

### Work Session Tracking

Future enhancement: Track individual work sessions to calculate actual work time automatically.

---

## 📊 Benefits

1. **Accurate Time Tracking**: Actual work hours reflect real effort
2. **Better Estimates**: Learning system gets accurate data to improve estimates
3. **Clear Work State**: Status always reflects current activity
4. **Prevents Inflated Metrics**: No more 500+ hour "completed" tasks

---

## 🔗 Related Documentation

- [Task Duration Estimation](./TASK_DURATION_ESTIMATION_IMPROVEMENTS.md)
- [Estimation Learning System](./ESTIMATION_LEARNING.md)
- [Daily Automation](./DAILY_AUTOMATION.md)

