import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { TableModule } from 'primeng/table';
import { ToastModule } from 'primeng/toast';
import { MessageService } from 'primeng/api';
import { UrlCheckService, URLCheck } from './url-check.service';
import { DatePipe, NgClass } from '@angular/common';
import { ChangeDetectorRef } from '@angular/core';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    FormsModule,
    ButtonModule,
    InputTextModule,
    TableModule,
    ToastModule,
    DatePipe,
    NgClass,
  ],
  providers: [MessageService],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
  url: string = '';
  checks: URLCheck[] = [];
  isNotLoaded: boolean = true;

  constructor(
    private service: UrlCheckService,
    private messageService: MessageService,
    private cd: ChangeDetectorRef,
  ) {}

  ngOnInit() {
    setTimeout(() => this.loadHistory(), 0);
  }

  loadHistory() {
    this.service.getAll().subscribe((data) => {
      this.checks = [...data];
      this.isNotLoaded = false;
      this.cd.detectChanges();
    });
  }

  checkUrl() {
    if (!this.url) {
      this.messageService.add({
        severity: 'warn',
        summary: 'Warning',
        detail: 'Please enter a URL',
      });
      return;
    }

    this.service.checkUrl(this.url).subscribe(
      (result) => {
        this.url = '';
        this.cd.markForCheck();
        this.loadHistory();
        this.cd.detectChanges();
        window.alert(`URL checked: ${result.verdict}`);
      },
      (error) => {
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to check URL',
        });
      },
    );
  }
}
