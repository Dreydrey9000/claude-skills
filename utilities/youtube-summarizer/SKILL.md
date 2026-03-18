---
name: youtube-summarizer
description: "Extract transcripts from YouTube videos and generate comprehensive, detailed summaries using intelligent analysis frameworks"
category: content
risk: safe
source: community
tags: "[video, summarization, transcription, youtube, content-analysis]"
date_added: "2026-02-27"
---

# youtube-summarizer

## Purpose

This skill extracts transcripts from YouTube videos and generates comprehensive, verbose summaries using the STAR + R-I-S-E framework. It validates video availability, extracts transcripts using the `youtube-transcript-api` Python library, and produces detailed documentation capturing all insights, arguments, and key points.

The skill is designed for users who need thorough content analysis and reference documentation from educational videos, lectures, tutorials, or informational content.

## When to Use This Skill

This skill should be used when:

- User provides a YouTube video URL and wants a detailed summary
- User needs to document video content for reference without rewatching
- User wants to extract insights, key points, and arguments from educational content
- User needs transcripts from YouTube videos for analysis
- User asks to "summarize", "resume", or "extract content" from YouTube videos
- User wants comprehensive documentation prioritizing completeness over brevity

## Main Workflow

### Progress Tracking Guidelines

Throughout the workflow, display a visual progress gauge before each step to keep the user informed. The gauge format is:

```bash
echo "[████░░░░░░░░░░░░░░░░] 20% - Step 1/5: Validating URL"
```

**Format specifications:**
- 20 characters wide (use █ for filled, ░ for empty)
- Percentage increments: Step 1=20%, Step 2=40%, Step 3=60%, Step 4=80%, Step 5=100%
- Step counter showing current/total (e.g., "Step 3/5")
- Brief description of current phase

**Display the initial status box before Step 1:**

```
╔══════════════════════════════════════════════════════════════╗
║     📹  YOUTUBE SUMMARIZER - Processing Video                ║
╠══════════════════════════════════════════════════════════════╣
║ → Step 1: Validating URL                 [IN PROGRESS]       ║
║ ○ Step 2: Checking Availability                              ║
║ ○ Step 3: Extracting Transcript                              ║
║ ○ Step 4: Generating Summary                                 ║
║ ○ Step 5: Formatting Output                                  ║
╠══════════════════════════════════════════════════════════════╣
║ Progress: ██████░░░░░░░░░░░░░░░░░░░░░░░░  20%               ║
╚══════════════════════════════════════════════════════════════╝
```

### Step 5: Format and Present Output

**Progress:**
```bash
echo "[████████████████████] 100% - Step 5/5: Formatting Output"
```

**Objective:** Deliver the summary in clean, well-structured Markdown.

**Output Structure:**

```markdown
# [Video Title]

**Canal:** [Channel Name]  
**Duração:** [Duration]  
**URL:** [https://youtube.com/watch?v=VIDEO_ID]  
**Data de Publicação:** [Date if available]


### [Topic 1]

[Comprehensive explanation with examples, data, quotes...]

#### [Subtopic 1.1]

[Detailed breakdown...]

### [Topic 2]

[Continued detailed analysis...]


## 📚 Concepts and Terminology

- **[Term 1]:** [Definition and context]
- **[Term 2]:** [Definition and context]


## 📌 Conclusion

[Final synthesis and takeaways]


### **Example 2: Missing Dependency**

**User Input:**
```
claude> summarize this youtube video https://youtu.be/abc123
```

**Skill Response:**

```
⚠️  youtube-transcript-api not installed

This skill requires the Python library 'youtube-transcript-api'.

Would you like me to install it now?
- [ ] Yes - Install with pip
- [ ] No - I'll install manually
```

**User selects "Yes":**

```bash
$ pip install youtube-transcript-api
Successfully installed youtube-transcript-api-0.6.1

✅ Installation complete! Proceeding with video summary...
```


### **Example 4: Invalid URL**

**User Input:**
```
claude> summarize youtube video www.youtube.com/some-video
```

**Skill Response:**

```
❌ Invalid YouTube URL format

Expected format examples:
- https://www.youtube.com/watch?v=VIDEO_ID
- https://youtu.be/VIDEO_ID

Please provide a valid YouTube video URL.
```


## 📊 Executive Summary

This video provides a comprehensive introduction to the fundamental concepts of Artificial Intelligence (AI), designed for beginners and professionals who want to understand the technical foundations and practical applications of modern AI. The instructor covers everything from basic definitions to machine learning algorithms, using practical examples and visualizations to facilitate understanding.

[... continued detailed summary ...]
```

**Save Options:**

```
What would you like to save?
→ Summary + raw transcript

✅ File saved: resumo-exemplo123-2026-02-01.md (includes raw transcript)
[████████████████████] 100% - ✓ Processing complete!
```


Welcome to this comprehensive tutorial on machine learning fundamentals. In today's video, we'll explore the core concepts that power modern AI systems...
```


**Version:** 1.2.0
**Last Updated:** 2026-02-02
**Maintained By:** Eric Andrade


## Full Specification

Complete details, decision trees, protocols, and implementation specs: [references/full-details.md](references/full-details.md)
