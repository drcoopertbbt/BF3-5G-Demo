'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from '@/components/ui/sheet'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Progress } from '@/components/ui/progress'
import { 
  CheckCircle, 
  XCircle, 
  AlertCircle, 
  Eye, 
  FileText, 
  Shield,
  ArrowRight
} from 'lucide-react'

interface ComplianceInspectorProps {
  procedureName: string
  isOpen: boolean
  onClose: () => void
}

export function ComplianceInspector({ procedureName, isOpen, onClose }: ComplianceInspectorProps) {
  // Mock 3GPP compliance data
  const specSteps = [
    { 
      id: 1, 
      name: 'Initial Registration Request', 
      status: 'completed', 
      specRef: 'TS 23.502 § 4.2.2.2.2',
      timestamp: '14:35:20.123'
    },
    { 
      id: 2, 
      name: 'Identity Request/Response', 
      status: 'completed', 
      specRef: 'TS 23.502 § 4.2.2.2.3',
      timestamp: '14:35:20.145'
    },
    { 
      id: 3, 
      name: 'Authentication', 
      status: 'completed', 
      specRef: 'TS 23.502 § 4.2.2.2.4',
      timestamp: '14:35:20.167'
    },
    { 
      id: 4, 
      name: 'Security Mode Command', 
      status: 'warning', 
      specRef: 'TS 23.502 § 4.2.2.2.5',
      timestamp: '14:35:20.189'
    },
    { 
      id: 5, 
      name: 'Registration Accept', 
      status: 'completed', 
      specRef: 'TS 23.502 § 4.2.2.2.6',
      timestamp: '14:35:20.201'
    },
  ]

  const payloadComparison = {
    '3gppRequired': {
      'messageType': 'Registration Request',
      '5gmmCapability': 'Mandatory',
      'ueSecurityCapability': 'Mandatory',
      'requestedNSSAI': 'Optional',
      'lastVisitedTAI': 'Optional',
      'ueUsageSetting': 'Optional'
    },
    'simulatorPayload': {
      'messageType': 'Registration Request',
      '5gmmCapability': '0x01',
      'ueSecurityCapability': '0x0001',
      'requestedNSSAI': 'Missing',
      'lastVisitedTAI': '0x012345',
      'customField': 'Non-standard'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircle className="w-4 h-4 text-green-500" />
      case 'warning': return <AlertCircle className="w-4 h-4 text-yellow-500" />
      case 'failed': return <XCircle className="w-4 h-4 text-red-500" />
      default: return <div className="w-4 h-4 rounded-full bg-gray-300" />
    }
  }

  const getComplianceColor = (field: string, value: string) => {
    if (value === 'Missing') return 'text-red-500'
    if (value === 'Non-standard') return 'text-yellow-500'
    if (field in payloadComparison['3gppRequired']) return 'text-green-500'
    return 'text-gray-500'
  }

  return (
    <Sheet open={isOpen} onOpenChange={onClose}>
      <SheetContent className="w-[800px] sm:max-w-[800px]">
        <SheetHeader>
          <SheetTitle className="flex items-center">
            <Shield className="w-5 h-5 mr-2" />
            3GPP Specification Inspector
          </SheetTitle>
          <SheetDescription>
            Procedure: {procedureName} - Real-time compliance validation
          </SheetDescription>
        </SheetHeader>

        <div className="mt-6 space-y-6">
          
          {/* Compliance Overview */}
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base">Compliance Overview</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-3 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">98.5%</div>
                  <div className="text-sm text-muted-foreground">Overall Compliance</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">4/5</div>
                  <div className="text-sm text-muted-foreground">Steps Validated</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-yellow-600">1</div>
                  <div className="text-sm text-muted-foreground">Warnings</div>
                </div>
              </div>
              <Progress value={98.5} className="mt-4" />
            </CardContent>
          </Card>

          <Tabs defaultValue="call-flow" className="w-full">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="call-flow">Call Flow Validation</TabsTrigger>
              <TabsTrigger value="payload">Payload Inspector</TabsTrigger>
            </TabsList>

            {/* Call Flow Validation */}
            <TabsContent value="call-flow" className="space-y-4">
              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-base">Procedure Steps vs 3GPP Specification</CardTitle>
                </CardHeader>
                <CardContent>
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead className="w-12">Status</TableHead>
                        <TableHead>Step</TableHead>
                        <TableHead>3GPP Reference</TableHead>
                        <TableHead>Timestamp</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {specSteps.map((step) => (
                        <TableRow key={step.id}>
                          <TableCell>{getStatusIcon(step.status)}</TableCell>
                          <TableCell className="font-medium">{step.name}</TableCell>
                          <TableCell>
                            <Badge variant="outline" className="text-xs">
                              {step.specRef}
                            </Badge>
                          </TableCell>
                          <TableCell className="font-mono text-xs">{step.timestamp}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Payload Inspector */}
            <TabsContent value="payload" className="space-y-4">
              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-base">Message Payload Comparison</CardTitle>
                  <CardDescription>Registration Request Message (Step 1)</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 gap-6">
                    
                    {/* 3GPP Required */}
                    <div>
                      <h4 className="font-medium mb-3 flex items-center">
                        <FileText className="w-4 h-4 mr-2" />
                        3GPP Required IEs
                      </h4>
                      <div className="space-y-2">
                        {Object.entries(payloadComparison['3gppRequired']).map(([field, requirement]) => (
                          <div key={field} className="flex justify-between items-center p-2 bg-muted rounded">
                            <span className="text-sm font-medium">{field}</span>
                            <Badge variant={requirement === 'Mandatory' ? 'default' : 'secondary'} className="text-xs">
                              {requirement}
                            </Badge>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Simulator Payload */}
                    <div>
                      <h4 className="font-medium mb-3 flex items-center">
                        <Activity className="w-4 h-4 mr-2" />
                        Simulator's Payload
                      </h4>
                      <div className="space-y-2">
                        {Object.entries(payloadComparison['simulatorPayload']).map(([field, value]) => (
                          <div key={field} className="flex justify-between items-center p-2 bg-muted rounded">
                            <span className="text-sm font-medium">{field}</span>
                            <span className={`text-xs font-mono ${getComplianceColor(field, value)}`}>
                              {value}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>

                  </div>

                  {/* Validation Summary */}
                  <div className="mt-6 p-4 bg-muted/50 rounded-lg">
                    <h5 className="font-medium mb-2">Validation Summary</h5>
                    <div className="grid grid-cols-3 gap-4 text-sm">
                      <div className="flex items-center space-x-2">
                        <CheckCircle className="w-4 h-4 text-green-500" />
                        <span>4 Fields Match</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <XCircle className="w-4 h-4 text-red-500" />
                        <span>1 Missing (Optional)</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <AlertCircle className="w-4 h-4 text-yellow-500" />
                        <span>1 Non-Standard</span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

          </Tabs>
        </div>
        
      </SheetContent>
    </Sheet>
  )
}

// Usage in parent component:
export function ComplianceButton({ procedureName }: { procedureName: string }) {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <Button 
        variant="outline" 
        size="sm" 
        onClick={() => setIsOpen(true)}
        className="flex items-center space-x-1"
      >
        <Shield className="w-4 h-4" />
        <span>3GPP Compliance</span>
      </Button>
      <ComplianceInspector 
        procedureName={procedureName}
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
      />
    </>
  )
}