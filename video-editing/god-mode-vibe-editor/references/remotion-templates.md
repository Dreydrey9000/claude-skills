# Remotion Component Templates

Copy-paste ready components for common viral video patterns.

## Base Video Composition

```typescript
// src/Video.tsx
import { AbsoluteFill, Video, staticFile, Sequence } from 'remotion';
import { TextOverlay } from './components/TextOverlay';
import { ProofCard } from './components/ProofCard';

export const ViralClip = () => {
  return (
    <AbsoluteFill className="bg-black">
      {/* Background Video */}
      <Video src={staticFile('footage/main.mp4')} />
      
      {/* Text Overlays */}
      <Sequence from={60} durationInFrames={90}>
        <TextOverlay text="10,000 VIDEOS" style="stat" />
      </Sequence>
      
      {/* Proof Card */}
      <Sequence from={150} durationInFrames={120}>
        <ProofCard 
          imagePath="screenshots/results.png"
          caption="Real results from last month"
        />
      </Sequence>
    </AbsoluteFill>
  );
};
```

---

## Text Overlay Component

```typescript
// src/components/TextOverlay.tsx
import { interpolate, useCurrentFrame, spring, useVideoConfig } from 'remotion';

type TextStyle = 'bold' | 'stat' | 'keyword' | 'cta';

interface TextOverlayProps {
  text: string;
  style?: TextStyle;
  position?: 'top' | 'center' | 'bottom';
  animation?: 'fade' | 'slide' | 'pop';
}

export const TextOverlay = ({ 
  text, 
  style = 'bold',
  position = 'bottom',
  animation = 'fade'
}: TextOverlayProps) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Animation values
  let opacity = 1;
  let translateY = 0;
  let scale = 1;

  if (animation === 'fade') {
    opacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' });
  } else if (animation === 'slide') {
    opacity = interpolate(frame, [0, 10], [0, 1], { extrapolateRight: 'clamp' });
    translateY = interpolate(frame, [0, 15], [50, 0], { extrapolateRight: 'clamp' });
  } else if (animation === 'pop') {
    scale = spring({ frame, fps, config: { damping: 10, stiffness: 100 } });
    opacity = interpolate(frame, [0, 5], [0, 1], { extrapolateRight: 'clamp' });
  }

  // Style variants
  const styles: Record<TextStyle, string> = {
    bold: 'text-5xl font-black text-white drop-shadow-[0_4px_8px_rgba(0,0,0,0.8)] uppercase tracking-wide',
    stat: 'text-7xl font-bold text-yellow-400 drop-shadow-[0_4px_8px_rgba(0,0,0,0.8)]',
    keyword: 'text-3xl font-semibold bg-black/60 px-6 py-3 rounded-xl',
    cta: 'text-4xl font-bold bg-gradient-to-r from-red-500 to-orange-500 px-8 py-4 rounded-2xl shadow-2xl',
  };

  // Position variants
  const positions = {
    top: 'top-20',
    center: 'top-1/2 -translate-y-1/2',
    bottom: 'bottom-32',
  };

  return (
    <div
      style={{
        opacity,
        transform: `translateY(${translateY}px) scale(${scale})`,
      }}
      className={`absolute left-1/2 -translate-x-1/2 ${positions[position]} ${styles[style]} text-center max-w-[90%]`}
    >
      {text}
    </div>
  );
};
```

---

## Proof Card Component

```typescript
// src/components/ProofCard.tsx
import { Img, staticFile, interpolate, useCurrentFrame, spring, useVideoConfig } from 'remotion';

interface ProofCardProps {
  imagePath: string;
  caption?: string;
  position?: 'top-right' | 'top-left' | 'center';
  size?: 'small' | 'medium' | 'large';
}

export const ProofCard = ({
  imagePath,
  caption,
  position = 'top-right',
  size = 'medium',
}: ProofCardProps) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 100 },
  });

  const opacity = interpolate(frame, [0, 10], [0, 1], { extrapolateRight: 'clamp' });

  const positions = {
    'top-right': 'top-10 right-10',
    'top-left': 'top-10 left-10',
    'center': 'top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2',
  };

  const sizes = {
    small: 'w-64',
    medium: 'w-80',
    large: 'w-96',
  };

  return (
    <div
      style={{ opacity, transform: `scale(${scale})` }}
      className={`absolute ${positions[position]} ${sizes[size]} bg-white rounded-2xl shadow-2xl overflow-hidden`}
    >
      <Img 
        src={staticFile(imagePath)} 
        className="w-full object-cover"
      />
      {caption && (
        <div className="p-4 bg-white">
          <p className="text-black font-semibold text-lg text-center">
            {caption}
          </p>
        </div>
      )}
    </div>
  );
};
```

---

## Zoom Pulse Component

```typescript
// src/components/ZoomPulse.tsx
import { interpolate, useCurrentFrame } from 'remotion';

interface ZoomPulseProps {
  intensity?: number;
  duration?: number;
}

export const ZoomPulse = ({ intensity = 1.15, duration = 10 }: ZoomPulseProps) => {
  const frame = useCurrentFrame();
  
  const scale = interpolate(
    frame,
    [0, duration / 2, duration],
    [1, intensity, 1],
    { extrapolateRight: 'clamp' }
  );

  return (
    <div 
      style={{ transform: `scale(${scale})` }}
      className="absolute inset-0 origin-center"
    />
  );
};
```

---

## Animated Counter Component

```typescript
// src/components/Counter.tsx
import { interpolate, useCurrentFrame } from 'remotion';

interface CounterProps {
  from: number;
  to: number;
  duration?: number;
  prefix?: string;
  suffix?: string;
  format?: 'number' | 'currency' | 'percent';
}

export const Counter = ({
  from,
  to,
  duration = 30,
  prefix = '',
  suffix = '',
  format = 'number',
}: CounterProps) => {
  const frame = useCurrentFrame();
  
  const value = interpolate(frame, [0, duration], [from, to], {
    extrapolateRight: 'clamp',
  });

  const formatValue = (val: number) => {
    switch (format) {
      case 'currency':
        return `$${Math.floor(val).toLocaleString()}`;
      case 'percent':
        return `${Math.floor(val)}%`;
      default:
        return Math.floor(val).toLocaleString();
    }
  };

  return (
    <span className="text-7xl font-black text-yellow-400 drop-shadow-lg">
      {prefix}{formatValue(value)}{suffix}
    </span>
  );
};
```

---

## Progress Bar Component

```typescript
// src/components/ProgressBar.tsx
import { interpolate, useCurrentFrame } from 'remotion';

interface ProgressBarProps {
  progress: number; // 0-100
  duration?: number;
  color?: string;
  label?: string;
}

export const ProgressBar = ({
  progress,
  duration = 30,
  color = '#22c55e',
  label,
}: ProgressBarProps) => {
  const frame = useCurrentFrame();
  
  const width = interpolate(frame, [0, duration], [0, progress], {
    extrapolateRight: 'clamp',
  });

  return (
    <div className="w-full max-w-md">
      {label && (
        <p className="text-white text-xl font-semibold mb-2">{label}</p>
      )}
      <div className="h-4 bg-white/20 rounded-full overflow-hidden">
        <div
          style={{ width: `${width}%`, backgroundColor: color }}
          className="h-full rounded-full transition-all"
        />
      </div>
      <p className="text-white text-lg font-bold mt-2 text-right">
        {Math.floor(width)}%
      </p>
    </div>
  );
};
```

---

## Subtitle Component (Karaoke Style)

```typescript
// src/components/Subtitle.tsx
import { useCurrentFrame, interpolate } from 'remotion';

interface Word {
  text: string;
  startFrame: number;
  endFrame: number;
}

interface SubtitleProps {
  words: Word[];
  highlightColor?: string;
}

export const Subtitle = ({ 
  words, 
  highlightColor = '#FFD700' 
}: SubtitleProps) => {
  const frame = useCurrentFrame();

  return (
    <div className="absolute bottom-20 left-0 right-0 text-center px-8">
      <p className="text-4xl font-bold leading-relaxed">
        {words.map((word, i) => {
          const isActive = frame >= word.startFrame && frame <= word.endFrame;
          const isPast = frame > word.endFrame;
          
          return (
            <span
              key={i}
              style={{
                color: isActive ? highlightColor : isPast ? '#ffffff' : '#ffffff80',
                transition: 'color 0.1s',
              }}
              className="drop-shadow-lg"
            >
              {word.text}{' '}
            </span>
          );
        })}
      </p>
    </div>
  );
};
```

---

## Intro/Outro Template

```typescript
// src/components/Intro.tsx
import { AbsoluteFill, Img, staticFile, interpolate, useCurrentFrame, spring, useVideoConfig } from 'remotion';

interface IntroProps {
  logoPath: string;
  title: string;
  subtitle?: string;
}

export const Intro = ({ logoPath, title, subtitle }: IntroProps) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const logoScale = spring({
    frame,
    fps,
    config: { damping: 15, stiffness: 100 },
  });

  const titleOpacity = interpolate(frame, [20, 35], [0, 1], { extrapolateRight: 'clamp' });
  const titleY = interpolate(frame, [20, 35], [30, 0], { extrapolateRight: 'clamp' });

  const subtitleOpacity = interpolate(frame, [35, 50], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill className="bg-gradient-to-br from-gray-900 to-black flex flex-col items-center justify-center">
      <Img
        src={staticFile(logoPath)}
        style={{ transform: `scale(${logoScale})` }}
        className="w-32 h-32 mb-8"
      />
      <h1
        style={{ opacity: titleOpacity, transform: `translateY(${titleY}px)` }}
        className="text-5xl font-black text-white text-center"
      >
        {title}
      </h1>
      {subtitle && (
        <p
          style={{ opacity: subtitleOpacity }}
          className="text-2xl text-white/70 mt-4"
        >
          {subtitle}
        </p>
      )}
    </AbsoluteFill>
  );
};
```

---

## Full Composition Example

```typescript
// src/Root.tsx
import { Composition } from 'remotion';
import { ViralClip } from './Video';

export const RemotionRoot = () => {
  return (
    <>
      <Composition
        id="ViralClip"
        component={ViralClip}
        durationInFrames={900} // 30 seconds at 30fps
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
```
