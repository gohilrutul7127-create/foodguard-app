import React, { useState, useRef } from 'react';
import {
  AlertTriangle,
  Camera,
  CheckCircle,
  Clock,
  Eye,
  FileImage,
  Flame,
  Info,
  Layers,
  Leaf,
  Loader2,
  PlusCircle,
  RefreshCw,
  Scan,
  ShieldAlert,
  ShieldCheck,
  Sparkles,
  Upload,
  X
} from 'lucide-react';
import { AppLayout } from './components/layout';
import { Button, Card } from './components/ui';
import { authenticatedRequest } from './auth';
import { useNavigate } from 'react-router-dom';

type FreshnessResult = {
  status: 'Fresh' | 'Moderate' | 'Spoiled';
  confidence: number;
  status_tone: 'safe' | 'warning' | 'danger';
  probabilities: {
    Fresh: number;
    Moderate: number;
    Spoiled: number;
  };
  summary: string;
  recommendation: string;
  action: string;
  metrics: {
    freshness_index: number;
    discoloration_score: number;
    texture_integrity: number;
    color_vibrancy: number;
  };
};

export function FoodFreshnessDetector() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<FreshnessResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const nav = useNavigate();

  const handleFileSelect = (selectedFile: File) => {
    if (!selectedFile.type.startsWith('image/')) {
      setError('Please upload a valid image file (JPEG, PNG, WEBP).');
      return;
    }
    setError(null);
    setFile(selectedFile);
    setPreviewUrl(URL.createObjectURL(selectedFile));
    setResult(null);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const runAnalysis = async () => {
    if (!file) return;
    setAnalyzing(true);
    setError(null);

    const formData = new FormData();
    formData.append('image', file);

    try {
      const res: FreshnessResult = await authenticatedRequest('/inventory/freshness-detect/', {
        method: 'POST',
        body: formData
      });
      setResult(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error analyzing image. Please try again.');
    } finally {
      setAnalyzing(false);
    }
  };

  // Helper to test with synthetic high-quality food samples immediately
  const loadDemoSample = (type: 'fresh' | 'moderate' | 'spoiled') => {
    const canvas = document.createElement('canvas');
    canvas.width = 400;
    canvas.height = 400;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    if (type === 'fresh') {
      // Vibrant green apple/produce
      const grad = ctx.createRadialGradient(200, 200, 30, 200, 200, 180);
      grad.addColorStop(0, '#86efac');
      grad.addColorStop(0.7, '#22c55e');
      grad.addColorStop(1, '#15803d');
      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.arc(200, 200, 160, 0, Math.PI * 2);
      ctx.fill();
    } else if (type === 'moderate') {
      // Ripening fruit with slight yellow-brown edges
      const grad = ctx.createRadialGradient(200, 200, 20, 200, 200, 180);
      grad.addColorStop(0, '#fef08a');
      grad.addColorStop(0.6, '#eab308');
      grad.addColorStop(1, '#854d0e');
      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.arc(200, 200, 160, 0, Math.PI * 2);
      ctx.fill();
      // add early spots
      ctx.fillStyle = '#713f12';
      ctx.beginPath();
      ctx.arc(140, 160, 18, 0, Math.PI * 2);
      ctx.arc(240, 230, 22, 0, Math.PI * 2);
      ctx.fill();
    } else {
      // Discolored / moldy item
      const grad = ctx.createRadialGradient(200, 200, 20, 200, 200, 180);
      grad.addColorStop(0, '#78716c');
      grad.addColorStop(0.6, '#57534e');
      grad.addColorStop(1, '#292524');
      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.arc(200, 200, 160, 0, Math.PI * 2);
      ctx.fill();
      // mold spots
      ctx.fillStyle = '#064e3b';
      ctx.beginPath();
      ctx.arc(160, 150, 40, 0, Math.PI * 2);
      ctx.arc(230, 220, 50, 0, Math.PI * 2);
      ctx.arc(180, 250, 35, 0, Math.PI * 2);
      ctx.fill();
    }

    canvas.toBlob((blob) => {
      if (blob) {
        const demoFile = new File([blob], `sample_${type}.jpg`, { type: 'image/jpeg' });
        handleFileSelect(demoFile);
      }
    }, 'image/jpeg');
  };

  const getStatusColor = (status: 'Fresh' | 'Moderate' | 'Spoiled') => {
    switch (status) {
      case 'Fresh':
        return {
          bg: 'bg-emerald-50 dark:bg-emerald-950/40',
          border: 'border-emerald-300 dark:border-emerald-800',
          text: 'text-emerald-700 dark:text-emerald-300',
          badge: 'bg-emerald-600 text-white',
          glow: 'shadow-emerald-500/20'
        };
      case 'Moderate':
        return {
          bg: 'bg-amber-50 dark:bg-amber-950/40',
          border: 'border-amber-300 dark:border-amber-800',
          text: 'text-amber-700 dark:text-amber-300',
          badge: 'bg-amber-500 text-white',
          glow: 'shadow-amber-500/20'
        };
      case 'Spoiled':
        return {
          bg: 'bg-rose-50 dark:bg-rose-950/40',
          border: 'border-rose-300 dark:border-rose-800',
          text: 'text-rose-700 dark:text-rose-300',
          badge: 'bg-rose-600 text-white',
          glow: 'shadow-rose-500/20'
        };
    }
  };

  return (
    <AppLayout>
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8 space-y-8">
        {/* Header Banner */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800">
                <Sparkles size={13} className="text-emerald-500" /> AI Vision Engine (TensorFlow & OpenCV)
              </span>
            </div>
            <h1 className="mt-2 text-3xl font-extrabold tracking-tight text-zinc-900 dark:text-zinc-50 sm:text-4xl">
              AI Food Freshness Detection
            </h1>
            <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
              Upload or snap a photo of produce, dairy, or pantry items to evaluate freshness, surface discoloration, and spoilage indicators.
            </p>
          </div>

          {/* Quick Demo Pre-sets */}
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-xs text-zinc-400 font-medium">Quick Demo:</span>
            <button
              onClick={() => loadDemoSample('fresh')}
              className="text-xs px-2.5 py-1 rounded-lg bg-emerald-100 dark:bg-emerald-950/50 text-emerald-800 dark:text-emerald-300 hover:bg-emerald-200 transition-colors"
            >
              Fresh
            </button>
            <button
              onClick={() => loadDemoSample('moderate')}
              className="text-xs px-2.5 py-1 rounded-lg bg-amber-100 dark:bg-amber-950/50 text-amber-800 dark:text-amber-300 hover:bg-amber-200 transition-colors"
            >
              Moderate
            </button>
            <button
              onClick={() => loadDemoSample('spoiled')}
              className="text-xs px-2.5 py-1 rounded-lg bg-rose-100 dark:bg-rose-950/50 text-rose-800 dark:text-rose-300 hover:bg-rose-200 transition-colors"
            >
              Spoiled
            </button>
          </div>
        </div>

        {error && (
          <div className="p-4 rounded-2xl bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900 text-rose-700 dark:text-rose-300 text-sm flex items-center gap-3">
            <AlertTriangle size={18} />
            <span>{error}</span>
          </div>
        )}

        {/* Main Grid: Upload & Preview on Left, Results on Right */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Left Column: Image Upload & Preview (5 cols) */}
          <div className="lg:col-span-5 space-y-6">
            <Card className="p-6 border border-zinc-200/80 dark:border-zinc-800 shadow-sm rounded-3xl bg-white/70 dark:bg-zinc-900/70 backdrop-blur-md">
              <h2 className="text-base font-bold text-zinc-900 dark:text-zinc-100 flex items-center gap-2">
                <Camera size={18} className="text-emerald-600" /> Upload Food Image
              </h2>
              <p className="text-xs text-zinc-500 mt-1">Take a clear photo with good lighting for best detection accuracy.</p>

              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                className="hidden"
                onChange={(e) => e.target.files?.[0] && handleFileSelect(e.target.files[0])}
              />

              {!previewUrl ? (
                <div
                  onDragOver={(e) => e.preventDefault()}
                  onDrop={handleDrop}
                  onClick={() => fileInputRef.current?.click()}
                  className="mt-4 border-2 border-dashed border-zinc-300 dark:border-zinc-700 hover:border-emerald-500 dark:hover:border-emerald-500 rounded-2xl p-8 flex flex-col items-center justify-center text-center cursor-pointer transition-colors bg-zinc-50/50 dark:bg-zinc-800/20 group"
                >
                  <div className="p-4 rounded-full bg-emerald-50 dark:bg-emerald-950/50 text-emerald-600 group-hover:scale-110 transition-transform">
                    <Upload size={28} />
                  </div>
                  <p className="mt-3 text-sm font-semibold text-zinc-700 dark:text-zinc-200">
                    Click to upload or drag & drop
                  </p>
                  <p className="text-xs text-zinc-400 mt-1">PNG, JPG, or WEBP up to 10MB</p>
                </div>
              ) : (
                <div className="mt-4 space-y-4">
                  <div className="relative rounded-2xl overflow-hidden border border-zinc-200 dark:border-zinc-800 bg-zinc-900 aspect-square flex items-center justify-center group">
                    <img src={previewUrl} alt="Food to scan" className="w-full h-full object-cover" />
                    
                    {/* Scanning laser beam animation when analyzing */}
                    {analyzing && (
                      <div className="absolute inset-0 bg-emerald-500/10 pointer-events-none">
                        <div className="w-full h-1 bg-gradient-to-r from-transparent via-emerald-400 to-transparent shadow-[0_0_15px_#10b981] animate-bounce" />
                      </div>
                    )}

                    <button
                      onClick={() => {
                        setFile(null);
                        setPreviewUrl(null);
                        setResult(null);
                      }}
                      className="absolute top-3 right-3 p-1.5 rounded-full bg-black/60 text-white hover:bg-black/80 transition-colors backdrop-blur-sm"
                    >
                      <X size={16} />
                    </button>
                  </div>

                  <div className="flex gap-3">
                    <Button
                      onClick={runAnalysis}
                      disabled={analyzing}
                      className="w-full py-2.5 font-semibold text-sm flex items-center justify-center gap-2 rounded-xl"
                    >
                      {analyzing ? (
                        <>
                          <Loader2 size={16} className="animate-spin" />
                          <span>Analyzing Visual Features…</span>
                        </>
                      ) : (
                        <>
                          <Scan size={16} />
                          <span>Detect Freshness</span>
                        </>
                      )}
                    </Button>
                    <button
                      onClick={() => fileInputRef.current?.click()}
                      className="px-3 py-2.5 rounded-xl border border-zinc-200 dark:border-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors text-zinc-600 dark:text-zinc-300"
                      title="Choose another image"
                    >
                      <RefreshCw size={16} />
                    </button>
                  </div>
                </div>
              )}
            </Card>
          </div>

          {/* Right Column: Prediction Display, Confidence Score, Visualization (7 cols) */}
          <div className="lg:col-span-7 space-y-6">
            {!result ? (
              <Card className="p-12 border border-zinc-200/80 dark:border-zinc-800 rounded-3xl bg-white/70 dark:bg-zinc-900/70 backdrop-blur-md flex flex-col items-center justify-center text-center">
                <div className="p-5 rounded-full bg-zinc-100 dark:bg-zinc-800 text-zinc-400">
                  <Scan size={44} />
                </div>
                <h3 className="mt-4 text-lg font-bold text-zinc-800 dark:text-zinc-200">
                  {analyzing ? 'Evaluating Food Freshness…' : 'No Food Scanned Yet'}
                </h3>
                <p className="mt-1 text-sm text-zinc-500 max-w-sm">
                  {analyzing
                    ? 'TensorFlow and OpenCV are decomposing color saturation, texture entropy, and necrotic spot density.'
                    : 'Upload an image on the left or select a quick demo sample to view real-time AI freshness diagnostics.'}
                </p>
              </Card>
            ) : (
              <div className="space-y-6 animate-fadeIn">
                {/* 1. Main Prediction Status Card */}
                {(() => {
                  const style = getStatusColor(result.status);
                  return (
                    <Card
                      className={`p-6 border ${style.border} ${style.bg} rounded-3xl shadow-lg ${style.glow} transition-all`}
                    >
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                        <div className="flex items-center gap-3.5">
                          <div className={`p-3 rounded-2xl ${style.badge}`}>
                            {result.status === 'Fresh' && <ShieldCheck size={28} />}
                            {result.status === 'Moderate' && <Clock size={28} />}
                            {result.status === 'Spoiled' && <ShieldAlert size={28} />}
                          </div>
                          <div>
                            <span className="text-xs uppercase font-extrabold tracking-wider opacity-75">
                              Model Prediction
                            </span>
                            <div className="flex items-center gap-2">
                              <h2 className={`text-3xl font-black ${style.text}`}>{result.status}</h2>
                              <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold ${style.badge}`}>
                                {result.confidence}% Confidence
                              </span>
                            </div>
                          </div>
                        </div>

                        {/* Quick Action Button */}
                        <Button
                          onClick={() => nav('/inventory')}
                          className="text-xs font-semibold px-4 py-2 rounded-xl flex items-center gap-1.5"
                        >
                          <PlusCircle size={14} /> Add to Inventory
                        </Button>
                      </div>

                      <div className="mt-5 pt-4 border-t border-black/10 dark:border-white/10 space-y-2">
                        <p className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">{result.summary}</p>
                        <p className="text-xs text-zinc-600 dark:text-zinc-300 leading-relaxed">{result.recommendation}</p>
                      </div>
                    </Card>
                  );
                })()}

                {/* 2. Confidence Probability Breakdown Meter */}
                <Card className="p-6 border border-zinc-200/80 dark:border-zinc-800 rounded-3xl bg-white/70 dark:bg-zinc-900/70 backdrop-blur-md">
                  <h3 className="text-sm font-bold text-zinc-900 dark:text-zinc-100 flex items-center gap-2">
                    <Layers size={16} className="text-blue-500" /> Class Probability Distribution
                  </h3>
                  <div className="mt-4 space-y-3">
                    <div>
                      <div className="flex justify-between text-xs font-medium mb-1">
                        <span className="text-emerald-700 dark:text-emerald-400 flex items-center gap-1">
                          <CheckCircle size={12} /> Fresh Probability
                        </span>
                        <span className="font-bold">{Math.round(result.probabilities.Fresh * 100)}%</span>
                      </div>
                      <div className="h-2.5 w-full bg-zinc-100 dark:bg-zinc-800 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-emerald-500 rounded-full transition-all duration-700"
                          style={{ width: `${Math.round(result.probabilities.Fresh * 100)}%` }}
                        />
                      </div>
                    </div>

                    <div>
                      <div className="flex justify-between text-xs font-medium mb-1">
                        <span className="text-amber-700 dark:text-amber-400 flex items-center gap-1">
                          <Clock size={12} /> Moderate / Early Ripening
                        </span>
                        <span className="font-bold">{Math.round(result.probabilities.Moderate * 100)}%</span>
                      </div>
                      <div className="h-2.5 w-full bg-zinc-100 dark:bg-zinc-800 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-amber-500 rounded-full transition-all duration-700"
                          style={{ width: `${Math.round(result.probabilities.Moderate * 100)}%` }}
                        />
                      </div>
                    </div>

                    <div>
                      <div className="flex justify-between text-xs font-medium mb-1">
                        <span className="text-rose-700 dark:text-rose-400 flex items-center gap-1">
                          <AlertTriangle size={12} /> Spoiled / Decay Detected
                        </span>
                        <span className="font-bold">{Math.round(result.probabilities.Spoiled * 100)}%</span>
                      </div>
                      <div className="h-2.5 w-full bg-zinc-100 dark:bg-zinc-800 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-rose-500 rounded-full transition-all duration-700"
                          style={{ width: `${Math.round(result.probabilities.Spoiled * 100)}%` }}
                        />
                      </div>
                    </div>
                  </div>
                </Card>

                {/* 3. Computer Vision & Sensory Feature Diagnostics */}
                <Card className="p-6 border border-zinc-200/80 dark:border-zinc-800 rounded-3xl bg-white/70 dark:bg-zinc-900/70 backdrop-blur-md">
                  <h3 className="text-sm font-bold text-zinc-900 dark:text-zinc-100 flex items-center gap-2">
                    <Eye size={16} className="text-emerald-500" /> Sensory & Feature Diagnostics
                  </h3>
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4">
                    <div className="p-3.5 rounded-2xl bg-zinc-50 dark:bg-zinc-800/60 border border-zinc-200/60 dark:border-zinc-700/60">
                      <span className="text-[11px] text-zinc-500 font-medium">Freshness Index</span>
                      <div className="text-xl font-bold mt-1 text-emerald-600 dark:text-emerald-400">
                        {result.metrics.freshness_index}%
                      </div>
                    </div>

                    <div className="p-3.5 rounded-2xl bg-zinc-50 dark:bg-zinc-800/60 border border-zinc-200/60 dark:border-zinc-700/60">
                      <span className="text-[11px] text-zinc-500 font-medium">Color Vibrancy</span>
                      <div className="text-xl font-bold mt-1 text-blue-600 dark:text-blue-400">
                        {result.metrics.color_vibrancy}%
                      </div>
                    </div>

                    <div className="p-3.5 rounded-2xl bg-zinc-50 dark:bg-zinc-800/60 border border-zinc-200/60 dark:border-zinc-700/60">
                      <span className="text-[11px] text-zinc-500 font-medium">Texture Integrity</span>
                      <div className="text-xl font-bold mt-1 text-purple-600 dark:text-purple-400">
                        {result.metrics.texture_integrity}%
                      </div>
                    </div>

                    <div className="p-3.5 rounded-2xl bg-zinc-50 dark:bg-zinc-800/60 border border-zinc-200/60 dark:border-zinc-700/60">
                      <span className="text-[11px] text-zinc-500 font-medium">Discoloration</span>
                      <div className="text-xl font-bold mt-1 text-rose-600 dark:text-rose-400">
                        {result.metrics.discoloration_score}%
                      </div>
                    </div>
                  </div>

                  <div className="mt-4 p-3.5 rounded-2xl bg-emerald-50/60 dark:bg-emerald-950/20 border border-emerald-200/60 dark:border-emerald-900/60 flex items-start gap-2.5 text-xs text-emerald-800 dark:text-emerald-300">
                    <Info size={15} className="mt-0.5 shrink-0" />
                    <span>
                      <strong>Recommendation:</strong> {result.action}
                    </span>
                  </div>
                </Card>
              </div>
            )}
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
