import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';
import { Button } from '../components/ui/Button';

interface Props {
  children: ReactNode;
  sectionName?: string;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error(`Uncaught error in ${this.props.sectionName || 'Application'}:`, error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="p-8 text-center glass-card border border-red-500/30 bg-red-500/5 my-4 space-y-4">
          <div className="p-3 rounded-full bg-red-500/10 text-red-400 w-fit mx-auto">
            <AlertTriangle className="w-6 h-6" />
          </div>
          <div className="space-y-1">
            <h3 className="text-base font-bold text-white">
              An error occurred in {this.props.sectionName || 'this component'}
            </h3>
            <p className="text-xs text-slate-400 font-mono">
              {this.state.error?.message || 'Unexpected application crash.'}
            </p>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={() => this.setState({ hasError: false, error: null })}
            leftIcon={<RefreshCw className="w-3.5 h-3.5" />}
          >
            Retry Section
          </Button>
        </div>
      );
    }

    return this.props.children;
  }
}
