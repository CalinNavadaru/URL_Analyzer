import { ChangeDetectorRef, Component, OnInit, signal } from '@angular/core';
import { URLCheck, UrlCheckService } from './url-check-service';
import { MessageService } from 'primeng/api';
import { TableModule } from 'primeng/table';
import { FormsModule } from '@angular/forms';
import { ButtonDirective } from 'primeng/button';
import { InputText } from 'primeng/inputtext';
import { Toast } from 'primeng/toast';
import { DatePipe, NgClass } from '@angular/common';

@Component({
  selector: 'app-root',
  imports: [TableModule, FormsModule, ButtonDirective, InputText, Toast, NgClass, DatePipe],
  providers: [MessageService],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App implements OnInit{
  url: string = '';
  checks: URLCheck[] = [];
  isNotLoaded: boolean = true;
  currentPage: number = 1;
  totalItems: number = 0;
  rowsPerPage: number = 5;

  constructor(
    private service: UrlCheckService,
    private messageService: MessageService,
    private cd: ChangeDetectorRef,
  ) {}

  ngOnInit() {
    setTimeout(() => this.loadHistory(1), 0);
  }

  loadHistory(page: number, size?: number) {
    this.service.getAll(page, size).subscribe((data) => {
      this.checks = data.results;
      this.totalItems = data.count;
      this.currentPage = page;
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
        this.loadHistory(this.currentPage, this.rowsPerPage);
        this.cd.detectChanges();
        window.alert(`URL checked: ${result.verdict}`);
      },
      (error) => {
        console.log(error);
        this.messageService.add({
          severity: 'error',
          summary: 'Failed to check URL',
          detail: error.error.error,
        });
      },
    );
  }

  onPageChange(event: any) {
    const page = event.first / event.rows + 1;
    this.rowsPerPage = event.rows;
    this.loadHistory(page, this.rowsPerPage);
  }
}
